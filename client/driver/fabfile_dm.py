import importlib
import json
import logging
import os
import re
import time
from collections import OrderedDict
from logging.handlers import RotatingFileHandler
from multiprocessing import Process

import requests
from fabric.api import lcd, local, task

from client.driver.utils import file_exists, get, get_content, run, run_sql_script, init_kubernetes_client, \
    exec_command_to_pod, copy_file_to_pod, check_db_ready

# Configure logging
LOG = logging.getLogger(__name__)


@task
def run_loops(max_iter=10, load=False, driver_config="driver_config", data=None):
    k8sapi = init_kubernetes_client()
    print("driver_config: {}".format(driver_config))
    dconf = load_driver_conf(driver_config, data)
    if load and dconf.DB_TYPE == 'dm':
        drop_user(dconf)
        create_user(dconf)
        load_sysbench(dconf)
        LOG.info('Run Load {}.'.format(dconf.BENCH_TYPE))
    # dump database if it's not done before.
    dump = dump_database(dconf)
    for i in range(int(max_iter)):
        # restart database
        restart_succeeded = restart_database(dconf, k8sapi)
        if not restart_succeeded:
            files = {'summary': b'{"error": "DB_RESTART_ERROR"}',
                     'knobs': b'{}',
                     'metrics_before': b'{}',
                     'metrics_after': b'{}'}
            if dconf.ENABLE_UDM:
                files['user_defined_metrics'] = b'{}'
            response = requests.post(dconf.WEBSITE_URL + '/new_result/', files=files,
                                     data={'upload_code': dconf.UPLOAD_CODE})
            response = get_result(dconf)
            result_timestamp = int(time.time())
            save_next_config(dconf, response, t=result_timestamp)
            change_conf(dconf, k8sapi, response['recommendation'])
            continue

        # reload database periodically
        if dconf.RELOAD_INTERVAL > 0:
            if i % dconf.RELOAD_INTERVAL == 0:
                if not is_ready_db(k8sapi, dconf):
                    raise Exception('database not ready!')
                if i == 0 and dump is False:
                    restore_database(dconf)
                elif i > 0:
                    restore_database(dconf)
        LOG.info('Wait %s seconds after restarting database', dconf.RESTART_SLEEP_SEC)
        if not is_ready_db(k8sapi, dconf):
            raise Exception('database not ready!')
        LOG.info('The %s-th Loop Starts / Total Loops %s', i + 1, max_iter)
        loop(i % dconf.RELOAD_INTERVAL if dconf.RELOAD_INTERVAL > 0 else i, dconf, k8sapi)
        LOG.info('The %s-th Loop Ends / Total Loops %s', i + 1, max_iter)


# 加载驱动配置
def load_driver_conf(driver_conf, data):
    mod = importlib.import_module(driver_conf)
    # 设定动态值
    mod.DB_HOST = data['host']
    mod.DB_POD_NAME = data['pod_name']
    mod.UPLOAD_CODE = data['upload_code']
    mod.CONTROLLER_CONFIG = os.path.join(mod.CONTROLLER_HOME, 'config/{}_{}_config.json'.format(mod.DB_TYPE, mod.UPLOAD_CODE))
    # Log files
    mod.DRIVER_LOG = os.path.join(mod.LOG_DIR, mod.UPLOAD_CODE, 'driver.log')
    mod.BENCH_LOG = os.path.join(mod.LOG_DIR, mod.UPLOAD_CODE, 'bench.log')
    mod.CONTROLLER_LOG = os.path.join(mod.LOG_DIR, mod.UPLOAD_CODE, 'controller.log')


    # Create local directories
    for _d in (os.path.join(mod.RESULT_DIR, mod.UPLOAD_CODE), os.path.join(mod.LOG_DIR, mod.UPLOAD_CODE),
               os.path.join(mod.TEMP_DIR, mod.UPLOAD_CODE)):
        os.makedirs(_d, exist_ok=True)

    LOG.setLevel(getattr(logging, mod.LOG_LEVEL, logging.DEBUG))
    Formatter = logging.Formatter(  # pylint: disable=invalid-name
        fmt='%(asctime)s [%(funcName)s:%(lineno)03d] %(levelname)-5s: %(message)s',
        datefmt='%m-%d-%Y %H:%M:%S')
    ConsoleHandler = logging.StreamHandler()  # pylint: disable=invalid-name
    ConsoleHandler.setFormatter(Formatter)
    LOG.addHandler(ConsoleHandler)
    FileHandler = RotatingFileHandler(  # pylint: disable=invalid-name
        mod.DRIVER_LOG, maxBytes=50000, backupCount=2)
    FileHandler.setFormatter(Formatter)
    LOG.addHandler(FileHandler)
    return mod


@task
def drop_user(dconf):
    run('/opt/dmdbms/bin/disql {}/{}@{}:{} -e "drop user IF EXISTS {} cascade"'.format(dconf.ADMIN_USER,
                                                                                       dconf.ADMIN_PWD,
                                                                                       dconf.DB_HOST,
                                                                                       dconf.DB_PORT,
                                                                                       dconf.DB_USER), capture=False)


@task
def create_user(dconf):
    run_sql_script(dconf, 'createUser.sh', dconf.ADMIN_USER, dconf.ADMIN_PWD, dconf.DB_USER,
                   dconf.DB_PASSWORD,
                   dconf.DB_HOST, dconf.DB_PORT)


@task
def load_sysbench(dconf):
    cmd = "./src/sysbench ./src/lua/oltp_read_write.lua --tables=250 --table-size=25000 --db-driver=dm --dm-db={}:{} --dm-user={} --dm-password={}  --auto-inc=1 --threads=128 --time=180 --report-interval=10 --thread-init-timeout=60 prepare > {}".format(
        dconf.DB_HOST, dconf.DB_PORT, dconf.DB_USER, dconf.DB_PASSWORD, dconf.BENCH_LOG)
    with lcd(dconf.SYSBENCH_HOME):  # pylint: disable=not-context-manager
        local(cmd)


# 数据dump导出
@task
def dump_database(dconf):
    dumpfile = os.path.join(dconf.DB_DUMP_DIR, dconf.UPLOAD_CODE, dconf.DB_NAME + '.dump')
    try:
        run_sql_script(dconf, 'dumpDm.sh', dconf.ADMIN_USER, dconf.ADMIN_PWD, dconf.DB_NAME,
                       os.path.join(dconf.DB_DUMP_DIR, dconf.UPLOAD_CODE),
                       dconf.DB_HOST,
                       dconf.DB_PORT)
        return True
    except Exception as e:
        return False


@task
def restart_database(dconf, api):
    return exec_command_to_pod(api=api, name=dconf.DB_POD_NAME, cmd='reload')


@task
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

        LOG.debug('%s\n\n[status code: %d, type(response): %s, elapsed: %ds, %s]', rout,
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

    LOG.info('Downloaded the next config in %ds', elapsed)
    return response_dict


@task
def save_next_config(dconf, next_config, t=None):
    if not t:
        t = int(time.time())
    with open(os.path.join(dconf.RESULT_DIR, dconf.UPLOAD_CODE, '{}__next_config.json'.format(t)), 'w') as f:
        json.dump(next_config, f, indent=2)
    return t


@task
def change_conf(dconf, api, next_conf=None):
    signal = "# configurations recommended by db-tune:\n"
    next_conf = next_conf or {}

    tmp_conf_ini = os.path.join(dconf.TEMP_DIR, dconf.UPLOAD_CODE, os.path.basename(dconf.DB_CONF))
    get(dconf, dconf.DB_CONF, tmp_conf_ini)
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

    # tmp_conf_out = os.path.join(dconf.TEMP_DIR, os.path.basename(dconf.DB_CONF) + '.out')
    with open(tmp_conf_ini, 'w') as f:
        f.write(''.join(lines))

    # 连接k8s cp文件至容器
    copy_file_to_pod(api=api, name=dconf.DB_POD_NAME, src_file=tmp_conf_ini, dest_file=dconf.REMOTE_DB_CONF)
    # 删除动态生成的.ini文件
    local('rm -f {}'.format(tmp_conf_ini))


@task
def is_ready_db(api, dconf):
    # 重试3次，每次RESTART_SLEEP_SEC秒
    for index in range(3):
        if check_db_ready(api=api, name=dconf.DB_POD_NAME):
            return True
        time.sleep(dconf.RESTART_SLEEP_SEC)
        if index == 2:
            return check_db_ready(api=api, name=dconf.DB_POD_NAME)


@task
def restore_database(dconf):
    """
    dump数据导入
    :param dconf: 配置文件
    :return:
    """
    dumpfile = os.path.join(dconf.DB_DUMP_DIR, dconf.DB_NAME + '.dump')
    if not file_exists(dumpfile):
        raise FileNotFoundError("Database dumpfile '{}' does not exist!".format(dumpfile))
    LOG.info('Start restoring database')
    drop_user()
    create_user()
    run_sql_script(dconf, 'restoreDm.sh', dconf.ADMIN_USER, dconf.ADMIN_PWD, dconf.DB_NAME, dumpfile, dconf.DB_HOST,
                   dconf.DB_PORT)


@task
def loop(i, dconf, api):
    i = int(i)

    # free cache
    free_cache(dconf, api)

    # remove oltpbench log and controller log
    clean_logs(dconf)

    if dconf.ENABLE_UDM is True:
        clean_bench_results()

    # check disk usage
    if check_disk_usage(dconf) > dconf.MAX_DISK_USAGE:
        LOG.warning('Exceeds max disk usage %s', dconf.MAX_DISK_USAGE)

    # run controller from another process
    p = Process(target=run_controller(dconf), args=())
    p.start()
    LOG.info('Run the controller')

    # run bench as a background job
    while not _ready_to_start_bench(dconf):
        time.sleep(1)
    run_sysbench(dconf)
    LOG.info('Run {}.'.format(dconf.BENCH_TYPE))

    # the controller starts the first collection
    while not _ready_to_start_controller(dconf):
        time.sleep(1)
    signal_controller(dconf)
    LOG.info('Start the first collection')

    # stop the experiment
    ready_to_shut_down = False
    error_msg = None
    while not ready_to_shut_down:
        ready_to_shut_down = _ready_to_shut_down_controller()
        time.sleep(1)

    signal_controller(dconf)
    LOG.info('Start the second collection, shut down the controller')

    p.join()
    if error_msg:
        raise Exception(dconf.BENCH_TYPE + ' Failed: ' + error_msg)
    # add user defined metrics
    if dconf.ENABLE_UDM is True:
        add_udm(dconf)

    # save result
    result_timestamp = save_dbms_result(dconf)

    if i >= dconf.WARMUP_ITERATIONS:
        # upload result
        upload_result(dconf)

        # get result
        response = get_result()

        # save next config
        save_next_config(response, t=result_timestamp)

        # change config
        change_conf(response['recommendation'])


@task
def free_cache(dconf, api):
    exec_command_to_pod(api=api, name=dconf.DB_POD_NAME, cmd='echo 3 > /proc/sys/vm/drop_caches')


def clean_logs(dconf):
    # remove oltpbench and controller log files
    local('rm -f {} {}'.format(dconf.BENCH_LOG, dconf.CONTROLLER_LOG))


@task
def clean_bench_results(dconf):
    # remove oltpbench result files
    local('rm -f {}/results/{}_outputfile.summary'.format(dconf.SYSBENCH_HOME, dconf.UPLOAD_CODE))


@task
def check_disk_usage(dconf):
    partition = dconf.DATABASE_DISK
    disk_use = 0
    if partition:
        cmd = "df -h {}".format(partition)
        out = run(cmd).splitlines()[1]
        m = re.search(r'\d+(?=%)', out)
        if m:
            disk_use = int(m.group(0))
        LOG.info("Current Disk Usage: %s%s", disk_use, '%')
    return disk_use


@task
def run_controller(dconf):
    LOG.info('Controller config path: %s', dconf.CONTROLLER_CONFIG)
    create_controller_config(dconf)
    cmd = 'gradle run -PappArgs="-c {} -t {} -p output/{} -d output/{}" --no-daemon > {}'.format(
        dconf.CONTROLLER_CONFIG,
        dconf.CONTROLLER_OBSERVE_SEC,
        dconf.UPLOAD_CODE,
        dconf.UPLOAD_CODE,
        dconf.CONTROLLER_LOG)
    with lcd(dconf.CONTROLLER_HOME):  # pylint: disable=not-context-manager
        local(cmd)


@task
def create_controller_config(dconf):
    dburl_fmt = 'jdbc:dm://{host}:{port}'.format

    config = dict(
        database_type=dconf.DB_TYPE,
        database_url=dburl_fmt(host=dconf.DB_HOST, port=dconf.DB_PORT, db=dconf.DB_NAME),
        username=dconf.DB_USER,
        password=dconf.DB_PASSWORD,
        upload_code='DEPRECATED',
        upload_url='DEPRECATED',
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


@task
def run_sysbench(dconf):
    if dconf.BENCH_TYPE.lower() == 'sysbench':
        cmd = "./src/sysbench ./src/lua/oltp_read_write.lua --tables=250 --table-size=25000 --db-driver=dm --dm-db={}:{} --dm-user={} --dm-password={}  --auto-inc=1 --threads=128 --time=180 --report-interval=10 --thread-init-timeout=60 --output-dir={} --output-name={}  run > {} 2>&1 &".format(
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


@task
def signal_controller(dconf):
    pidfile = os.path.join(dconf.CONTROLLER_HOME, dconf.UPLOAD_CODE, 'pid.txt')
    with open(pidfile, 'r') as f:
        pid = int(f.read())
    cmd = 'kill -2 {}'.format(pid)
    with lcd(dconf.CONTROLLER_HOME):  # pylint: disable=not-context-manager
        local(cmd)


def _ready_to_shut_down_controller(dconf):
    pidfile = os.path.join(dconf.CONTROLLER_HOME, dconf.UPLOAD_CODE, 'pid.txt')
    ready = False
    if os.path.exists(pidfile) and os.path.exists(dconf.BENCH_LOG):
        with open(dconf.BENCH_LOG, 'r') as f:
            content = f.read()
            if 'failed' in content:
                m = re.search('\n.*Error.*\n', content)
                error_msg = m.group(0)
                LOG.error('{} Failed!'.format(dconf.BENCH_TYPE))
                return True, error_msg
            else:
                ready = 'SQL statistics:' in content
    return ready


@task
def add_udm(dconf):
    # result_dir = os.path.join(dconf.CONTROLLER_HOME, 'output')
    with lcd(dconf.UDM_DIR):  # pylint: disable=not-context-manager
        local('python3 user_defined_metrics.py {}'.format(dconf.__name__))


@task
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


@task
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
    if response.status_code != 200:
        raise Exception('Error uploading result.\nStatus: {}\nMessage: {}\n'.format(
            response.status_code, get_content(response)))

    for f in files.values():  # pylint: disable=not-an-iterable
        f.close()

    LOG.info(get_content(response))
    return response
