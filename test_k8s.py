from kubernetes import client, config

# Configs can be set in Configuration class directly or using helper utility
from kubernetes.stream import stream

config.load_kube_config(config_file="./admin.conf")

api = client.CoreV1Api()
print("Listing pods with their IPs:")
ret = api.list_pod_for_all_namespaces(watch=False)
for i in ret.items:
    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

exec_command = ['/bin/sh', '-c', 'nc -z localhost 5236;echo $?']
resp = stream(api.connect_get_namespaced_pod_exec,
              name='dm1547852714717470720-0',
              namespace='dmcp-instance',
              container='database',
              command=exec_command,
              stderr=True, stdin=False,
              stdout=True, tty=False)
print("Response: " + resp)

# Copying file
# source_file = '/Users/Administrator/Desktop/source-code/ottertune/admin.conf'
# destination_file = '/usr/share/filebeat/admin.conf'
#
# exec_command = ['/bin/sh']
# resp = stream(api.connect_get_namespaced_pod_exec, 'dm-log-beat-filebeat-7hnhp', 'dmcp-system',
#               command=exec_command,
#               stderr=True, stdin=True,
#               stdout=True, tty=False,
#               _preload_content=False)
#
# # file = open(source_file, "r")
# #
# # commands = []
# # commands.append("cat <<'EOF' >" + destination_file + "\n")
# # commands.append(file.read())
# # commands.append("EOF\n")
#
#
# buf = b''
# with open(source_file, "rb") as file:
#     buf += file.read()
# file.close()
#
# commands = [bytes("cat <<'EOF' >" + destination_file + "\n", 'utf-8'), buf, bytes("EOF\n", 'utf-8')]
#
# while resp.is_open():
#     resp.update(timeout=1)
#     if resp.peek_stdout():
#         print("STDOUT: %s" % resp.read_stdout())
#     if resp.peek_stderr():
#         print("STDERR: %s" % resp.read_stderr())
#     if commands:
#         c = commands.pop(0)
#         print("Running command... %s\n" % c)
#         resp.write_stdin(c)
#     else:
#         break
# resp.close()
