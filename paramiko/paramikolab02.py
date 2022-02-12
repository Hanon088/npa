from http import client
import time
import paramiko
username = 'admin'
password = 'cisco'
key_file="C:\\Users\\Jack\\Documents\\NPA\\rsa2"
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

        ssh.send("conf t\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)

        """ssh.send(f"int g0/1\nip addr {g01}\nno shut\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)

        ssh.send(f"int g0/2\nip addr {g02}\nno shut\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)"""

        """ssh.send("router ospf 1 vrf control-Data\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)

        for network in networks:
            ssh.send(f"network {network} area 0\n")
            time.sleep(1)
            result = ssh.recv(1000).decode('ascii')
            print(result)
        
        if ip == "172.31.104.6":
            ssh.send("default-information originate\n")
            time.sleep(1)
            result = ssh.recv(1000).decode('ascii')
            print(result)

        ssh.send("exit\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)"""

        ssh.send("ip access-list extended telnetSSH\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)

        ssh.send("permit tcp 172.31.104.0 0.0.0.15 any eq 23\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)

        ssh.send("permit tcp 10.253.190.0 0.0.0.255 any eq 23\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)

        ssh.send("permit tcp 172.31.104.0 0.0.0.15 any eq 22\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)

        ssh.send("permit tcp 10.253.190.0 0.0.0.255 any eq 22\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)

        ssh.send("exit\nline vty 0 4\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)

        ssh.send("access-class telnetSSH in vrf-also\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)

        ssh.send("end\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)

        if ip == "172.31.104.6":
            ssh.send("conf t\nip access-list standard controlData\n")
            time.sleep(1)
            result = ssh.recv(1000).decode('ascii')
            print(result)

            ssh.send("deny 172.31.104.0 0.0.0.15\n")
            time.sleep(1)
            result = ssh.recv(1000).decode('ascii')
            print(result)

            ssh.send("permit 172.31.104.0 0.0.0.255\nexit\n")
            time.sleep(1)
            result = ssh.recv(1000).decode('ascii')
            print(result)

            ssh.send("ip nat inside source list controlData interface g0/2 vrf control-Data overload\n")
            time.sleep(1)
            result = ssh.recv(1000).decode('ascii')
            print(result)

            ssh.send("int g0/1\nip nat inside\n")
            time.sleep(1)
            result = ssh.recv(1000).decode('ascii')
            print(result)

            ssh.send("int g0/2\nip nat outside\n")
            time.sleep(1)
            result = ssh.recv(1000).decode('ascii')
            print(result)

            ssh.send("end\n")
            time.sleep(1)
            result = ssh.recv(1000).decode('ascii')
            print(result)

        """ssh.send("sh ip inter br\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)"""
