import telnetlib
import time
import getpass
host = ["172.31.104.4", "172.31.104.5", "172.31.104.6"]
user = "admin"
password = getpass.getpass()
ip = ["1.1.1.1","2.2.2.2","3.3.3.3"]

# tn_session = telnetlib.Telnet(host, 23, 5)

# tn_session.read_until(b"Username:")
# tn_session.write(user.encode('ascii') + b"\n")
# time.sleep(1)

# tn_session.read_until(b"Password:")
# tn_session.write(password.encode() + b"\n")

# tn_session.write(b"show ip interface br\n")
# time.sleep(2)
# tn_session.write(b"exit\n")
# time.sleep(1)
# output = tn_session.read_very_eager()
# print(output.decode('ascii'))

# tn_session.close()

def config_loopback(password,host,ip):
    """config loopback for r1 r2 r3"""
    tn_session = telnetlib.Telnet(host, 23, 5)

    tn_session.read_until(b"Username:")
    tn_session.write("admin".encode('ascii')+ b"\n")
    time.sleep(1)

    tn_session.read_until(b"Password:")
    tn_session.write(password.encode('ascii')+ b"\n")
    time.sleep(1)

    tn_session.write(b"enable" + b"\n")
    time.sleep(1)
    print("in to previlage")
    tn_session.read_until(b"#")
    tn_session.write(b"config ter" + b"\n")
    time.sleep(1)
    print("in to config terminal")
    tn_session.read_until(b"(config)")
    tn_session.write(b"interface loopback 0" + b"\n")
    time.sleep(1)
    print("in to interface config")
    tn_session.read_until(b"(config-if)")
    tn_session.write(b"ip address " + ip.encode('ascii') + b" 255.255.255.0\n")
    time.sleep(1)
    print("config ip sucess")
    tn_session.write(b"end\n")
    tn_session.write(b"show ip interface br" + b"\n")
    time.sleep(1)
    tn_session.write(b"exit\n")
    result = tn_session.read_very_eager()
    tn_session.close()
    return result
for host_ip in range(0,3):
    print(config_loopback(password,host[host_ip],ip[host_ip]).decode('ascii'))
