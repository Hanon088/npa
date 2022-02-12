from http import client
import time
import paramiko
username = 'admin'
password = 'cisco'
key_file="C:\\Users\\Jack\\Documents\\NPA\\rsa2"

devices = [['172.31.104.4', ['172.31.104.17 255.255.255.240', '172.31.104.33 255.255.255.240']],
          ['172.31.104.5', ['172.31.104.34 255.255.255.240', '172.31.104.49 255.255.255.240']],
          ['172.31.104.6', ['172.31.104.50 255.255.255.240', 'dhcp']]]

for device in devices:
    ip = device[0]
    g01 = device[1][0]
    g02 = device[1][1]
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

        ssh.send("conf t\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)

        ssh.send(f"int g0/1\nip addr {g01}\nno shut\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)

        ssh.send(f"int g0/2\nip addr {g02}\nno shut\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)

        ssh.send("end\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)

        ssh.send("sh ip inter br\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)
