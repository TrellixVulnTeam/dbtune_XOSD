import os
import sys
import tarfile
from os.path import abspath, dirname, join, basename
from tempfile import TemporaryFile

import requests
from django.http import QueryDict, HttpRequest
from django.utils.datastructures import MultiValueDict
from fabric.api import get as _get, put as _put, run as _run, sudo as _sudo
from fabric.api import local
from kubernetes import client, config
from kubernetes.stream import stream

# 绝对路径
BASE_DIR = dirname(abspath(__file__))


def parse_bool(value):
    if not isinstance(value, bool):
        value = str(value).lower() == 'true'
    return value


def get_content(response):
    content_type = response.headers.get('Content-Type', '')
    if content_type == 'application/json':
        content = response.json()
    else:
        content = response.content
        if isinstance(content, bytes):
            content = content.decode('utf-8')
    return content


def run(dconf, cmd, capture=True, remote_only=False, **kwargs):
    capture = parse_bool(capture)

    try:
        if dconf.HOST_CONN == 'remote':
            res = _run(cmd, **kwargs)
        elif dconf.HOST_CONN == 'local':
            res = local(cmd, capture=capture, **kwargs)
        else:  # docker or remote_docker
            opts = ''
            cmdd = cmd
            if cmd.endswith('&'):
                cmdd = cmd[:-1].strip()
                opts = '-d '
            if remote_only:
                docker_cmd = cmdd
            else:
                docker_cmd = 'docker exec {} -ti {} /bin/bash -c "{}"'.format(
                    opts, dconf.CONTAINER_NAME, cmdd)
            if dconf.HOST_CONN == 'docker':
                res = local(docker_cmd, capture=capture, **kwargs)
            elif dconf.HOST_CONN == 'remote_docker':
                res = _run(docker_cmd, **kwargs)
            else:
                raise Exception('wrong HOST_CONN type {}'.format(dconf.HOST_CONN))
    except TypeError as e:
        err = str(e).strip()
        if 'unexpected keyword argument' in err:
            offender = err.rsplit(' ', 1)[-1][1:-1]
            kwargs.pop(offender)
            res = run(dconf, cmd, **kwargs)
        else:
            raise e
    return res


def get(conf, remote_path, local_path, use_sudo=False):
    use_sudo = parse_bool(use_sudo)

    if conf.HOST_CONN == 'remote':
        res = _get(remote_path, local_path, use_sudo=use_sudo)
    elif conf.HOST_CONN == 'local':
        pre_cmd = 'sudo ' if use_sudo else ''
        opts = '-r' if os.path.isdir(remote_path) else ''
        res = local('{}cp {} {} {}'.format(pre_cmd, opts, remote_path, local_path))
    else:  # docker or remote_docker
        docker_cmd = 'docker cp -L {}:{} {}'.format(conf.CONTAINER_NAME, remote_path, local_path)
        if conf.HOST_CONN == 'docker':
            if conf.DB_CONF_MOUNT is True:
                pre_cmd = 'sudo ' if use_sudo else ''
                opts = '-r' if os.path.isdir(remote_path) else ''
                res = local('{}cp {} {} {}'.format(pre_cmd, opts, remote_path, local_path))
            else:
                res = local(docker_cmd)
        elif conf.HOST_CONN == 'remote_docker':
            pre_cmd = 'sudo ' if use_sudo else ''
            opts = '-r' if os.path.isdir(remote_path) else ''
            res = local('{}cp {} {} {}'.format(pre_cmd, opts, remote_path, local_path))
        else:
            raise Exception('wrong HOST_CONN type {}'.format(conf.HOST_CONN))
    return res


def put(dconf, local_path, remote_path, use_sudo=False):
    use_sudo = parse_bool(use_sudo)

    if dconf.HOST_CONN == 'remote':
        res = _put(local_path, remote_path, use_sudo=use_sudo)
    elif dconf.HOST_CONN == 'local':
        pre_cmd = 'sudo ' if use_sudo else ''
        opts = '-r' if os.path.isdir(local_path) else ''
        res = local('{}cp {} {} {}'.format(pre_cmd, opts, local_path, remote_path))
    else:  # docker or remote_docker
        docker_cmd = 'docker cp -L {} {}:{}'.format(local_path, dconf.CONTAINER_NAME, remote_path)
        if dconf.HOST_CONN == 'docker':
            if dconf.DB_CONF_MOUNT is True:
                pre_cmd = 'sudo ' if use_sudo else ''
                opts = '-r' if os.path.isdir(local_path) else ''
                res = local('{}cp {} {} {}'.format(pre_cmd, opts, local_path, remote_path))
            else:
                res = local(docker_cmd)
        elif dconf.HOST_CONN == 'remote_docker':
            if dconf.DB_CONF_MOUNT is True:
                res = _put(local_path, remote_path, use_sudo=use_sudo)
            else:
                res = _put(local_path, local_path, use_sudo=use_sudo)
                res = sudo(dconf, docker_cmd, remote_only=True)
        else:
            raise Exception('wrong HOST_CONN type {}'.format(dconf.HOST_CONN))
    return res


def sudo(dconf, cmd, user=None, capture=True, remote_only=False, **kwargs):
    capture = parse_bool(capture)

    if dconf.HOST_CONN == 'remote':
        res = _sudo(cmd, user=user, **kwargs)

    elif dconf.HOST_CONN == 'local':
        pre_cmd = 'sudo '
        if user:
            pre_cmd += '-u {} '.format(user)
        res = local(pre_cmd + cmd, capture=capture, **kwargs)

    else:  # docker or remote_docker
        user = user or 'root'
        opts = '-ti -u {}'.format(user or 'root')
        if user == 'root':
            opts += ' -w /'
        if remote_only:
            docker_cmd = cmd
        else:
            docker_cmd = 'docker exec {} {} /bin/bash -c "{}"'.format(
                opts, dconf.CONTAINER_NAME, cmd)
        if dconf.HOST_CONN == 'docker':
            res = local(docker_cmd, capture=capture, **kwargs)
        elif dconf.HOST_CONN == 'remote_docker':
            res = _sudo(docker_cmd, **kwargs)
        else:
            raise Exception('wrong HOST_CONN type {}'.format(dconf.HOST_CONN))
    return res


def run_sql_script(conf, script_file, *args):
    scriptdir = join(BASE_DIR, 'dmScripts')
    remote_path = join(scriptdir, script_file)
    if not file_exists(conf, remote_path):
        run(conf, 'mkdir -p {}'.format(scriptdir))
        put(conf, os.path.join('./dmScripts', script_file), remote_path)
    return run(conf, 'sh {} {}'.format(remote_path, ' '.join(args)))


def file_exists(conf, filename):
    # with settings(warn_only=True), hide('warnings'):  # pylint: disable=not-context-manager
    # res = run(conf, '[ ls -l {} ]'.format(filename))
    return os.path.exists(filename)


class FabricException(Exception):
    pass


def init_kubernetes_client(config_file="/etc/kubernetes/kubernetes.conf"):
    """
    init k8s client
    :param config_file: kubernetes的配置文件
    :return: kubernetes client对象
    """
    config.load_kube_config(config_file=config_file)
    return client.CoreV1Api()


def check_db_ready(dconf, api, namespace="dmcp-instance", name=None, container="database"):
    """
    检查数据库状态是否正常
    :return: False: 服务不正常  True：服务正常
    """
    exec_command = ['/bin/sh', '-c', 'nc -z ' + dconf.DB_HOST + ' ' + dconf.DB_PORT + ';echo $?']
    try:
        resp = stream(api.connect_get_namespaced_pod_exec,
                      name=name,
                      namespace=namespace,
                      container=container,
                      command=exec_command,
                      stderr=True, stdin=False,
                      stdout=True, tty=False)
        print("check_db_ready Response: [{}]".format(resp))
        if resp == 1:
            return False
    except Exception as e:
        print("check_db_ready err: \n {}".format(e))
        raise Exception("check_db_ready err! {}".format(e))
        # return False
    return True


def exec_command_to_pod(api, namespace="dmcp-instance", name=None, container="database", cmd=None):
    """
    在容器中执行操作
    """
    exec_command = ['/bin/sh', '-c', cmd]
    try:
        resp = stream(api.connect_get_namespaced_pod_exec,
                      name=name,
                      namespace=namespace,
                      container=container,
                      command=exec_command,
                      stderr=True, stdin=False,
                      stdout=True, tty=False)
        print("exec_command_to_pod Response: \n {}".format(resp))
    except Exception as e:
        print("exec_command_to_pod err: \n {}".format(e))
        raise Exception("exec_command_to_pod err! {}".format(e))
        # return False
    return True


def copy_file_to_pod(api, namespace="dmcp-instance", name=None, container="database", src_file=None,
                     dest_file=None):
    """
    从本地拷贝文件到容器中
    """
    try:
        exec_command = ['/bin/sh']
        resp = stream(api.connect_get_namespaced_pod_exec,
                      name=name,
                      namespace=namespace,
                      container=container,
                      command=exec_command,
                      stderr=True, stdin=True,
                      stdout=True, tty=False,
                      _preload_content=False)

        buffer = b''
        with open(src_file, "rb") as file:
            buffer += file.read()
        file.close()

        commands = [bytes("cat <<'EOF' >" + dest_file + "\n", 'utf-8'), buffer, bytes("EOF\n", 'utf-8')]

        while resp.is_open():
            resp.update(timeout=1)
            if resp.peek_stdout():
                print("STDOUT: %s" % resp.read_stdout())
            if resp.peek_stderr():
                print("STDERR: %s" % resp.read_stderr())
            if commands:
                c = commands.pop(0)
                # print("Running command... %s\n" % c)
                resp.write_stdin(c)
            else:
                break
        resp.close()
    except Exception as e:
        print("copy_file_to_pod err: \n {}".format(e))
        raise Exception("copy_file_to_pod err! {}".format(e))


def copy_file_from_pod(api, namespace="dmcp-instance", name=None, container="database", src_file=None,
                       dest_path=None):
    """
    从容器中拷贝文件到本地
    """
    try:
        dir = dirname(src_file)
        bname = basename(src_file)
        exec_command = ['/bin/sh', '-c',
                        'cd {src}; tar cf - {base}'.format(src=dir, base=bname)]
        with TemporaryFile() as tar_buffer:
            resp = stream(api.connect_get_namespaced_pod_exec,
                          name=name,
                          namespace=namespace,
                          container=container,
                          command=exec_command,
                          stderr=True, stdin=True,
                          stdout=True, tty=False,
                          _preload_content=False)

            while resp.is_open():
                resp.update(timeout=1)
                if resp.peek_stdout():
                    out = resp.read_stdout()
                    # print("STDOUT: %s" % len(out))
                    tar_buffer.write(out.encode('utf-8'))
                if resp.peek_stderr():
                    print('STDERR: {0}'.format(resp.read_stderr()))
            resp.close()

            tar_buffer.flush()
            tar_buffer.seek(0)

            with tarfile.open(fileobj=tar_buffer, mode='r:') as tar:
                subdir_and_files = [
                    tarinfo for tarinfo in tar.getmembers()
                ]
                def is_within_directory(directory, target):
                    
                    abs_directory = os.path.abspath(directory)
                    abs_target = os.path.abspath(target)
                
                    prefix = os.path.commonprefix([abs_directory, abs_target])
                    
                    return prefix == abs_directory
                
                def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                
                    for member in tar.getmembers():
                        member_path = os.path.join(path, member.name)
                        if not is_within_directory(path, member_path):
                            raise Exception("Attempted Path Traversal in Tar File")
                
                    tar.extractall(path, members, numeric_owner) 
                    
                
                safe_extract(tar, path=dest_path, members=subdir_and_files)
    except Exception as e:
        print("copy_file_from_pod err: {}".format(e))
        raise Exception("copy_file_from_pod err! {}".format(e))
