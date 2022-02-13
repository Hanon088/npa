from http import client
import time
import paramiko
username = 'admin'
password = 'cisco'
key_file="rsa2" #march
# key_file="C:\\Users\\Jack\\Documents\\NPA\\rsa2" #jack
# [ip, [g01, g02], [ospf networks]]
devices = [['172.31.104.4', ['172.31.104.17 255.255.255.240', '172.31.104.33 255.255.255.240'], ['1.1.1.1 0.0.0.0', '172.31.104.16 0.0.0.15', '172.31.104.32 0.0.0.15']],
          ['172.31.104.5', ['172.31.104.34 255.255.255.240', '172.31.104.49 255.255.255.240'], ['2.2.2.2 0.0.0.0', '172.31.104.32 0.0.0.15', '172.31.104.48 0.0.0.15']],
          ['172.31.104.6', ['172.31.104.50 255.255.255.240', 'dhcp'], ['3.3.3.3 0.0.0.0', '172.31.104.48 0.0.0.15']]]

for device in devices:
    ip = device[0]
    g01 = device[1][0]
    g02 = device[1][1]
    networks = device[2]
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
        # start config terminal
        ssh.send("conf t\n")

        # set ip interface g0/1
        ssh.send(f"int g0/1\nip addr {g01}\nno shut\n")

        # set ip interface g0/2
        ssh.send(f"int g0/2\nip addr {g02}\nno shut\n")

        # start set ospf in vrf controll-data
        ssh.send("router ospf 1 vrf control-Data\n")

        for network in networks:
            ssh.send(f"network {network} area 0\n")

        # ospf default route gen on r3
        if ip == "172.31.104.6":
            ssh.send("default-information originate\n")

        ssh.send("exit\n")
        # start set acl for allow pc1 to control-datplane not management plane
        ssh.send("ip access-list extended telnetSSH\n")
        ssh.send("permit tcp 172.31.104.0 0.0.0.15 any eq 23\n")
        ssh.send("permit tcp 10.253.190.0 0.0.0.255 any eq 23\n")
        ssh.send("permit tcp 172.31.104.0 0.0.0.15 any eq 22\n")
        ssh.send("permit tcp 10.253.190.0 0.0.0.255 any eq 22\n")
        ssh.send("exit\nline vty 0 4\n")

        # allow ssh from management plane
        ssh.send("access-class telnetSSH in vrf-also\n")
        ssh.send("end\n")
        #R3 acl
        if ip == "172.31.104.6":
            ssh.send("conf t\nip access-list standard controlData\n")
            ssh.send("deny 172.31.104.0 0.0.0.15\n")
            ssh.send("permit 172.31.104.0 0.0.0.255\nexit\n")

            #set pat on r3
            ssh.send("ip nat inside source list controlData interface g0/2 vrf control-Data overload\n")
            ssh.send("int g0/1\nip nat inside\n")
            ssh.send("int g0/2\nip nat outside\n")
            ssh.send("end\n")

        ssh.send("do sh run\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)
