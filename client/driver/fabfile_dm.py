import importlib
import json
import logging
import os
import re
import time
from collections import OrderedDict
from logging.handlers import TimedRotatingFileHandler

import requests
from fabric.api import lcd, local

from server.website.website.mq.producter import push_msg
from .userDefinedMetrics.user_defined_metrics_dm import add_udm
from .utils_dm import file_exists, get_content, run, run_sql_script, init_kubernetes_client, \
    exec_command_to_pod, copy_file_to_pod, check_db_ready, copy_file_from_pod


def run_loops(max_iter=10, load=False, driver_config="driver_config", data=None):
    try:
        k8sapi = init_kubernetes_client()
        print("driver_config: {}".format(driver_config))
        dconf = load_driver_conf(driver_config, data)
        if load and dconf.DB_TYPE == 'dm':
            dconf.LOG.info('Run drop user[{}] IF EXISTS.'.format(dconf.DB_USER))
            drop_user(dconf)
            dconf.LOG.info('Run create user[{}].'.format(dconf.DB_USER))
            create_user(dconf)
            dconf.LOG.info('Run clean {}.'.format(dconf.BENCH_TYPE))
            clean_sysbench(dconf)
            dconf.LOG.info('Run Load {}.'.format(dconf.BENCH_TYPE))
            load_sysbench(dconf)
        # dump database if it's not done before.
        dconf.LOG.info('Run dump database.')
        dump = dump_database(dconf)
        for i in range(int(max_iter)):
            dconf.LOG.info('Run restart database.')
            # restart database
            restart_succeeded = restart_database(dconf, k8sapi)
            if not restart_succeeded:
                dconf.LOG.error('restart database error, please check k8s connect! task exit...')
                raise Exception('restart_database error, please check k8s connect!')

            # reload database periodically
            if dconf.RELOAD_INTERVAL > 0:
                if i % dconf.RELOAD_INTERVAL == 0:
                    if not is_ready_db(k8sapi, dconf):
                        raise Exception('database not ready!')
                    if i == 0 and dump is False:
                        restore_database(dconf)
                    elif i > 0:
                        restore_database(dconf)
            dconf.LOG.info('Wait %s seconds after restarting database', dconf.RESTART_SLEEP_SEC)
            if not is_ready_db(k8sapi, dconf):
                raise Exception('database not ready!')
            dconf.LOG.info('The %s-th Loop Starts / Total Loops %s', i + 1, max_iter)
            loop(i % dconf.RELOAD_INTERVAL if dconf.RELOAD_INTERVAL > 0 else i, dconf, k8sapi)
            dconf.LOG.info('The %s-th Loop Ends / Total Loops %s', i + 1, max_iter)
    except Exception as e:
        msg = dict(message="failed to recommended configuration! {}".format(e), status="FAILURE", id=dconf.DB_ID,
                   recommendation=None, performance=None)
        # 推送消息至队列
        push_msg(json.dumps(msg))


# 加载驱动配置
def load_driver_conf(driver_conf, data):
    mod = importlib.import_module(driver_conf)
    # 设定动态值
    mod.DB_HOST = data['host']
    mod.DB_PORT = str(data['port']) if data['port'] is not None else '5236'
    mod.DB_POD_NAME = data['pod_name']
    mod.DB_ID = data['db_id']
    mod.UPLOAD_CODE = data['upload_code']
    mod.CONTROLLER_CONFIG = os.path.join(mod.CONTROLLER_HOME,
                                         'config/{}_{}_config.json'.format(mod.DB_TYPE, mod.UPLOAD_CODE))
    # dconf.LOG files
    # mod.DRIVER_LOG = os.path.join(mod.LOG_DIR, mod.UPLOAD_CODE, 'driver.dconf.LOG')
    mod.DRIVER_LOG = os.path.join(mod.LOG_DIR, 'driver.log')
    mod.BENCH_LOG = os.path.join(mod.LOG_DIR, mod.UPLOAD_CODE, 'bench.log')
    mod.CONTROLLER_LOG = os.path.join(mod.LOG_DIR, mod.UPLOAD_CODE, 'controller.log')

    # Create local directories
    for _d in (os.path.join(mod.RESULT_DIR, mod.UPLOAD_CODE), os.path.join(mod.LOG_DIR, mod.UPLOAD_CODE),
               os.path.join(mod.TEMP_DIR, mod.UPLOAD_CODE), os.path.join(mod.DB_DUMP_DIR, mod.UPLOAD_CODE)):
        os.makedirs(_d, exist_ok=True)

    log = logging.getLogger(__name__)
    log.setLevel(getattr(logging, mod.LOG_LEVEL, logging.DEBUG))
    Formatter = logging.Formatter(  # pylint: disable=invalid-name
        fmt='%(asctime)s [%(funcName)s:%(lineno)03d] \033[1;31m%(levelname)-5s \033[1;33m[' + mod.UPLOAD_CODE + '] \033[1;32m%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    ConsoleHandler = logging.StreamHandler()  # pylint: disable=invalid-name
    ConsoleHandler.setFormatter(Formatter)
    log.addHandler(ConsoleHandler)
    FileHandler = TimedRotatingFileHandler(
        mod.DRIVER_LOG, when='MIDNIGHT', interval=1, encoding='utf-8')
    # FileHandler = RotatingFileHandler(  # pylint: disable=invalid-name
    #     mod.DRIVER_LOG, maxBytes=50000, backupCount=2)
    FileHandler.setFormatter(Formatter)
    log.addHandler(FileHandler)
    mod.LOG = log
    # dconf.LOG = dconf.LOG
    # dconf.LOG = dconf.LOG(mod.DRIVER_LOG, mod.UPLOAD_CODE)
    return mod


def drop_user(dconf):
    cmd = '/opt/dmdbms/bin/disql {}/{}@{}:{} -e "drop user IF EXISTS {} cascade"'.format(dconf.ADMIN_USER,
                                                                                         dconf.ADMIN_PWD,
                                                                                         dconf.DB_HOST,
                                                                                         dconf.DB_PORT,
                                                                                         dconf.DB_USER)
    # with lcd("/opt/dmdbms/bin"):  # pylint: disable=not-context-manager
    res = local(cmd, capture=True)
    if res.failed:
        dconf.LOG.error('drop user Failed!')
        raise Exception("drop user Failed!{}\n".format(res.stderr))
    # run(dconf=dconf,
    #     cmd='/opt/dmdbms/bin/disql {}/{}@{}:{} -e "drop user IF EXISTS {} cascade"'.format(dconf.ADMIN_USER,
    #                                                                                        dconf.ADMIN_PWD,
    #                                                                                        dconf.DB_HOST,
    #                                                                                        dconf.DB_PORT,
    #                                                                                        dconf.DB_USER),
    #     capture=False)


def create_user(dconf):
    run_sql_script(dconf, 'createUser.sh', dconf.ADMIN_USER, dconf.ADMIN_PWD, dconf.DB_USER,
                   dconf.DB_PASSWORD,
                   dconf.DB_HOST, dconf.DB_PORT)


def clean_sysbench(dconf):
    cmd = "./sysbench ./oltp_read_write.lua --tables=25 --table-size=2500 --db-driver=dm --dm-db={}:{} --dm-user={} --dm-password={}  --auto-inc=1 --threads=128 --time=180 --report-interval=10 --thread-init-timeout=60 cleanup > {}".format(
        dconf.DB_HOST, dconf.DB_PORT, dconf.DB_USER, dconf.DB_PASSWORD, dconf.BENCH_LOG)
    with lcd(dconf.SYSBENCH_HOME):  # pylint: disable=not-context-manager
        res = local(cmd, True)
        if res.failed:
            dconf.LOG.error('clean sysbench Failed!')
            raise Exception("clean sysbench Failed!{}\n".format(res.stderr))


def load_sysbench(dconf):
    cmd = "./sysbench ./oltp_read_write.lua --tables=25 --table-size=2500 --db-driver=dm --dm-db={}:{} --dm-user={} --dm-password={}  --auto-inc=1 --threads=128 --time=180 --report-interval=10 --thread-init-timeout=60 prepare > {}".format(
        dconf.DB_HOST, dconf.DB_PORT, dconf.DB_USER, dconf.DB_PASSWORD, dconf.BENCH_LOG)
    with lcd(dconf.SYSBENCH_HOME):  # pylint: disable=not-context-manager
        res = local(cmd, True)
        if res.failed:
            dconf.LOG.error('load sysbench Failed!')
            raise Exception("Failed load sysbench!{}\n".format(res.stderr))


# 数据dump导出
def dump_database(dconf):
    dumpfile = os.path.join(dconf.DB_DUMP_DIR, dconf.UPLOAD_CODE, dconf.DB_NAME + '.dump')
    if file_exists(dconf, dumpfile):
        dconf.LOG.info('%s already exists ! ', dumpfile)
        return False
    try:
        run_sql_script(dconf, 'dumpDm.sh', dconf.ADMIN_USER, dconf.ADMIN_PWD, dconf.DB_NAME,
                       os.path.join(dconf.DB_DUMP_DIR, dconf.UPLOAD_CODE),
                       dconf.DB_HOST,
                       dconf.DB_PORT)
        return True
    except Exception as e:
        raise Exception("dump database err! {}".format(e))


def restart_database(dconf, api):
    # 重试3次，每次1秒
    for index in range(3):
        try:
            if exec_command_to_pod(api=api, name=dconf.DB_POD_NAME, cmd='/usr/local/bin/reload'):
                return True
            time.sleep(1)
        except Exception as e:
            dconf.LOG.warning("restart database failed, retry %s/3...", index + 1)
        try:
            if index == 2: return exec_command_to_pod(api=api, name=dconf.DB_POD_NAME, cmd='/usr/local/bin/reload')
        except Exception as e:
            dconf.LOG.error("restart database failed! %s", e)
            return False


def get_result(dconf, max_time_sec=180, interval_sec=5, upload_code=None):
    max_time_sec = int(max_time_sec)
    interval_sec = int(interval_sec)
    upload_code = upload_code or dconf.UPLOAD_CODE
    url = dconf.WEBSITE_URL + '/query_and_get/' + upload_code
    elapsed = 0
    response_dict = None
    rout = ''

    while elapsed <= max_time_sec:
        rsp = requests.get(url)
        response = get_content(rsp)
        assert response != 'null'
        rout = json.dumps(response, indent=4) if isinstance(response, dict) else response

        dconf.LOG.debug('%s\n\n[status code: %d, type(response): %s, elapsed: %ds, %s]', rout,
                        rsp.status_code, type(response), elapsed,
                        ', '.join(['{}: {}'.format(k, v) for k, v in rsp.headers.items()]))

        if rsp.status_code == 200:
            # Success
            response_dict = response
            break

        elif rsp.status_code == 202:
            # Not ready
            time.sleep(interval_sec)
            elapsed += interval_sec

        elif rsp.status_code == 400:
            # Failure
            raise Exception(
                "Failed to download the next config.\nStatus code: {}\nMessage: {}\n".format(
                    rsp.status_code, rout))

        elif rsp.status_code == 500:
            # Failure
            msg = rout
            raise Exception(
                "Failed to download the next config.\nStatus code: {}\nMessage: {}\n".format(
                    rsp.status_code, msg))

        else:
            raise NotImplementedError(
                "Unhandled status code: '{}'.\nMessage: {}".format(rsp.status_code, rout))

    if not response_dict:
        assert elapsed > max_time_sec, \
            'response={} but elapsed={}s <= max_time={}s'.format(
                rout, elapsed, max_time_sec)
        raise Exception(
            'Failed to download the next config in {}s: {} (elapsed: {}s)'.format(
                max_time_sec, rout, elapsed))

    dconf.LOG.info('Downloaded the next config in %ds', elapsed)
    return response_dict


def save_next_config(dconf, next_config, t=None):
    if not t:
        t = int(time.time())
    with open(os.path.join(dconf.RESULT_DIR, dconf.UPLOAD_CODE, '{}__next_config.json'.format(t)), 'w') as f:
        json.dump(next_config, f, indent=2)
    return t


def change_conf(dconf, api, next_conf=None):
    signal = "# configurations recommended by db-tune:\n"
    next_conf = next_conf or {}

    tmp_conf_path = os.path.join(dconf.TEMP_DIR, dconf.UPLOAD_CODE)
    tmp_conf_ini = os.path.join(tmp_conf_path, dconf.DB_CONF)
    # 将远程容器中的配置拷贝到本地
    copy_file_from_pod(api=api, name=dconf.DB_POD_NAME, src_file=dconf.REMOTE_DB_CONF, dest_path=tmp_conf_path)
    with open(tmp_conf_ini, 'r') as f:
        lines = f.readlines()
    f.close()

    if signal not in lines:
        lines += ['\n', signal]

    signal_idx = lines.index(signal)
    lines = lines[0:signal_idx + 1]

    if isinstance(next_conf, str):
        with open(next_conf, 'r') as f:
            recommendation = json.load(f, encoding="UTF-8", object_pairs_hook=OrderedDict)['recommendation']
    else:
        recommendation = next_conf

    assert isinstance(recommendation, dict)

    for name, value in recommendation.items():
        lines.append('{} = {}\n'.format(name, value))
    lines.append('\n')

    with open(tmp_conf_ini, 'w') as f:
        f.write(''.join(lines))

    # 连接k8s cp文件至容器
    copy_file_to_pod(api=api, name=dconf.DB_POD_NAME, src_file=tmp_conf_ini, dest_file=dconf.REMOTE_DB_CONF)
    # 删除动态生成的.ini文件
    local('rm -f {}'.format(tmp_conf_ini))


def is_ready_db(api, dconf):
    # 重试3次，每次RESTART_SLEEP_SEC秒
    for index in range(3):
        try:
            if check_db_ready(dconf, api=api, name=dconf.DB_POD_NAME):
                return True
            time.sleep(dconf.RESTART_SLEEP_SEC)
        except Exception as e:
            dconf.LOG.warning("db not ready, retry %s/3...", index + 1)
        try:
            if index == 2: return check_db_ready(dconf, api=api, name=dconf.DB_POD_NAME)
        except Exception as e:
            return False


def restore_database(dconf):
    """
    dump数据导入
    :param dconf: 配置文件
    :return:
    """
    dumpfile = os.path.join(dconf.DB_DUMP_DIR, dconf.UPLOAD_CODE, dconf.DB_NAME + '.dump')
    if not file_exists(dconf, dumpfile):
        raise FileNotFoundError("Database dumpfile '{}' does not exist!".format(dumpfile))
    dconf.LOG.info('Start restoring database')
    drop_user(dconf)
    create_user(dconf)
    run_sql_script(dconf, 'restoreDm.sh', dconf.ADMIN_USER, dconf.ADMIN_PWD, dconf.DB_NAME, dumpfile, dconf.DB_HOST,
                   dconf.DB_PORT)


def loop(i, dconf, api):
    i = int(i)

    dconf.LOG.info('Run free cache.')
    # free cache
    free_cache(dconf, api)

    dconf.LOG.info('Run clean logs.')
    # remove oltpbench dconf.LOG and controller dconf.LOG
    clean_logs(dconf)

    if dconf.ENABLE_UDM is True:
        dconf.LOG.info('Run clean bench results.')
        clean_bench_results(dconf)

    dconf.LOG.info('Run check disk usage.')
    # check disk usage
    if check_disk_usage(dconf) > dconf.MAX_DISK_USAGE:
        dconf.LOG.warning('Exceeds max disk usage %s', dconf.MAX_DISK_USAGE)

    # run controller from another process
    # p = Process(target=run_controller(dconf), args=())
    # p.start()
    dconf.LOG.info('Run the controller')
    run_controller(dconf)

    # run bench as a background job
    while not _ready_to_start_bench(dconf):
        time.sleep(1)
    dconf.LOG.info('Run {}.'.format(dconf.BENCH_TYPE))
    run_sysbench(dconf)

    start = time.time()
    # the controller starts the first collection
    while not _ready_to_start_controller(dconf):
        time.sleep(1)
        end = time.time()
        if end - start > dconf.RELOAD_INTERVAL:
            dconf.LOG.error('run sysbench Failed!')
            raise Exception("run sysbench Failed!")

    dconf.LOG.info('Start the first collection')
    signal_controller(dconf)

    # stop the experiment
    ready_to_shut_down = False
    error_msg = None
    start = time.time()
    while not ready_to_shut_down:
        ready_to_shut_down, error_msg = _ready_to_shut_down_controller(dconf)
        time.sleep(1)
        end = time.time()
        if end - start > dconf.SYSBENCH_TIMEOUT:
            dconf.LOG.error('get sysbench result Failed!')
            raise Exception("get sysbench result Failed!")

    dconf.LOG.info('Start the second collection, shut down the controller')
    signal_controller(dconf)

    # p.join()
    if error_msg:
        raise Exception(dconf.BENCH_TYPE + ' Failed: ' + error_msg)
    # add user defined metrics
    if dconf.ENABLE_UDM is True:
        dconf.LOG.info('Run add user_defined_metrics.')
        add_udm(dconf)

    time.sleep(3)

    dconf.LOG.info('Run save dbms dataset.')
    # save result
    result_timestamp = save_dbms_result(dconf)

    if i >= dconf.WARMUP_ITERATIONS:
        dconf.LOG.info('Run upload dbms dataset.')
        # upload result
        upload_result(dconf)

        dconf.LOG.info('Run get next config(recommendation params).')
        # get result
        response = get_result(dconf)

        dconf.LOG.info('Run save next config(recommendation params).')
        # save next config
        save_next_config(dconf, response, t=result_timestamp)

        dconf.LOG.info('Run change dbms config.')
        # change config
        change_conf(dconf, api, response['recommendation'])


def free_cache(dconf, api):
    exec_command_to_pod(api=api, name=dconf.DB_POD_NAME, cmd='echo 3 > /proc/sys/vm/drop_caches')


def clean_logs(dconf):
    # remove oltpbench and controller dconf.LOG files
    local('rm -f {} {}'.format(dconf.CONTROLLER_CONFIG, dconf.CONTROLLER_LOG))


def clean_bench_results(dconf):
    # remove oltpbench result files
    local('rm -f {}/results/{}_outputfile.summary'.format(dconf.SYSBENCH_HOME, dconf.UPLOAD_CODE))


def check_disk_usage(dconf):
    partition = dconf.DATABASE_DISK
    disk_use = 0
    if partition:
        cmd = "df -h {}".format(partition)
        out = run(dconf, cmd).splitlines()[1]
        m = re.search(r'\d+(?=%)', out)
        if m:
            disk_use = int(m.group(0))
        dconf.LOG.info("Current Disk Usage: %s%s", disk_use, '%')
    return disk_use


def run_controller(dconf, interval_sec=-1):
    dconf.LOG.info('Controller config path: %s', dconf.CONTROLLER_CONFIG)
    create_controller_config(dconf)
    # cmd = 'gradle run -PappArgs="-c {} -t {} -p output/{} -d output/{}" --no-daemon > {}'.format(
    cmd = 'nohup java -jar controller.jar -c {} -t {} -p output/{} -d output/{} > {} 2>&1 &'.format(
        dconf.CONTROLLER_CONFIG,
        interval_sec,
        dconf.UPLOAD_CODE,
        dconf.UPLOAD_CODE,
        dconf.CONTROLLER_LOG)
    with lcd(dconf.CONTROLLER_HOME):  # pylint: disable=not-context-manager
        local(cmd)


def create_controller_config(dconf):
    dburl_fmt = 'jdbc:dm://{host}:{port}'.format

    config = dict(
        database_type=dconf.DB_TYPE,
        database_url=dburl_fmt(host=dconf.DB_HOST, port=dconf.DB_PORT, db=dconf.DB_NAME),
        username=dconf.DB_USER,
        password=dconf.DB_PASSWORD,
        upload_code=dconf.UPLOAD_CODE,
        upload_url=dconf.WEBSITE_URL,
        # upload_code='DEPRECATED',
        # upload_url='DEPRECATED',
        workload_name=dconf.OLTPBENCH_BENCH if dconf.BENCH_TYPE != 'sysbench' else dconf.BENCH_TYPE
    )

    with open(dconf.CONTROLLER_CONFIG, 'w') as f:
        json.dump(config, f, indent=2)


def _ready_to_start_bench(dconf):
    ready = False
    if os.path.exists(dconf.CONTROLLER_LOG):
        with open(dconf.CONTROLLER_LOG, 'r') as f:
            content = f.read()
        ready = 'Output the process pid to' in content
    return ready


def run_sysbench(dconf):
    if dconf.BENCH_TYPE.lower() == 'sysbench':
        cmd = "./sysbench ./oltp_read_write.lua --tables=25 --table-size=2500 --db-driver=dm --dm-db={}:{} --dm-user={} --dm-password={}  --auto-inc=1 --threads=128 --time=60 --report-interval=10 --thread-init-timeout=60 --output-dir={} --output-name={}  run > {} 2>&1 &".format(
            dconf.DB_HOST, dconf.DB_PORT, dconf.DB_USER, dconf.DB_PASSWORD,
            os.path.join(dconf.SYSBENCH_HOME, "results"),
            dconf.UPLOAD_CODE + "_outputfile.summary",
            dconf.BENCH_LOG)
        with lcd(dconf.SYSBENCH_HOME):  # pylint: disable=not-context-manager
            local(cmd)


def _ready_to_start_controller(dconf):
    ready = False
    if os.path.exists(dconf.BENCH_LOG):
        with open(dconf.BENCH_LOG, 'r') as f:
            content = f.read()
            if 'failed' in content:
                ready = True
            else:
                ready = 'Threads started!' in content
    return ready


def signal_controller(dconf):
    pidfile = os.path.join(dconf.CONTROLLER_HOME, 'output', dconf.UPLOAD_CODE, 'pid.txt')
    with open(pidfile, 'r') as f:
        pid = int(f.read())
    cmd = 'kill -2 {}'.format(pid)
    with lcd(dconf.CONTROLLER_HOME):  # pylint: disable=not-context-manager
        local(cmd)


def _ready_to_shut_down_controller(dconf):
    pidfile = os.path.join(dconf.CONTROLLER_HOME, 'output', dconf.UPLOAD_CODE, 'pid.txt')
    ready = False
    if os.path.exists(pidfile) and os.path.exists(dconf.BENCH_LOG):
        with open(dconf.BENCH_LOG, 'r') as f:
            content = f.read()
            if 'failed' in content:
                m = re.search('\n.*Error.*\n', content)
                error_msg = m.group(0)
                dconf.LOG.error('{} Failed!'.format(dconf.BENCH_TYPE))
                return True, error_msg
            else:
                ready = 'SQL statistics:' in content
    return ready, None


def save_dbms_result(dconf):
    t = int(time.time())
    files = ['knobs.json', 'metrics_after.json', 'metrics_before.json', 'summary.json']
    if dconf.ENABLE_UDM:
        files.append('user_defined_metrics.json')
    for f_ in files:
        srcfile = os.path.join(dconf.CONTROLLER_HOME, 'output', dconf.UPLOAD_CODE, f_)
        dstfile = os.path.join(dconf.RESULT_DIR, dconf.UPLOAD_CODE, '{}__{}'.format(t, f_))
        local('cp {} {}'.format(srcfile, dstfile))
    return t


def upload_result(dconf):
    result_dir = os.path.join(dconf.CONTROLLER_HOME, 'output', dconf.UPLOAD_CODE)
    prefix = ''
    upload_code = dconf.UPLOAD_CODE
    files = {}
    bases = ['summary', 'knobs', 'metrics_before', 'metrics_after']
    if dconf.ENABLE_UDM:
        bases.append('user_defined_metrics')
    for base in bases:
        fpath = os.path.join(result_dir, prefix + base + '.json')

        # Replaces the true db version with the specified version to allow for
        # testing versions not officially supported by OtterTune
        if base == 'summary' and dconf.OVERRIDE_DB_VERSION:
            with open(fpath, 'r') as f:
                summary = json.load(f)
            summary['real_database_version'] = summary['database_version']
            summary['database_version'] = dconf.OVERRIDE_DB_VERSION
            with open(fpath, 'w') as f:
                json.dump(summary, f, indent=1)

        files[base] = open(fpath, 'rb')
    response = requests.post(dconf.WEBSITE_URL + '/new_result/', files=files,
                             data={'upload_code': upload_code})

    # response = upload_results(files=files, data={'upload_code': upload_code})
    if response.status_code != 200:
        raise Exception('Error uploading result.\nStatus: {}\nMessage: {}\n'.format(
            response.status_code, get_content(response)))

    for f in files.values():  # pylint: disable=not-an-iterable
        f.close()

    dconf.LOG.info("upload_result: %s", get_content(response))
    return response
