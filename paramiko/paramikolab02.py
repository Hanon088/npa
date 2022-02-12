from http import client
import time
import paramiko
username = 'admin'
password = 'cisco'
key_file="C:\\Users\\Jack\\Documents\\NPA\\rsa2"

device_ip = ['172.31.104.4','172.31.104.5','172.31.104.6']
for ip in device_ip:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key = paramiko.RSAKey.from_private_key_file(key_file)
    client.connect(hostname=ip, port=22, username=username, pkey=key, look_for_keys=False)
    print("connecting to {} ...".format(ip))
    with client.invoke_shell() as ssh:
        ssh.send("terminal length 0\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)

        ssh.send("sh ip inter br\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)
