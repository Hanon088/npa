import re
import telnetlib
import time
import getpass

def start_seesion(host_ip, Username, Password):
    """start telnet seesion"""
    tn_session = telnetlib.Telnet(host_ip, 23, 5)
    tn_session.read_until(b"Username:")
    tn_session.write(Username.encode('ascii')+ b"\n")
    time.sleep(1)

    tn_session.read_until(b"Password:")
    tn_session.write(Password.encode('ascii')+ b"\n")
    time.sleep(1)

    return tn_session
def config_ip_interface(tn_session, ip, netmask, interface):
    """config ip interface"""
    tn_session.read_until(b"#")
    tn_session.write(b"config ter\n")
    time.sleep(1)
    print("in to config terminal")

    tn_session.read_until(b"(config)")
    tn_session.write(b"interface " + interface.encode('ascii') + b"\n")
    time.sleep(1)

    tn_session.read_until(b"(config-if)")
    tn_session.write(b"ip address " + ip.encode('ascii') +b" " + netmask.encode('ascii') + b"\n")
    time.sleep(1)

    tn_session.write(b"no shutdown\n")
    time.sleep(1)

    tn_session.write(b"end\n")
    tn_session.write(b"sh ip interface br\n")
    time.sleep(1)

    result = tn_session.read_very_eager()
    return result

def main():
    """r1 ip config to 172.31.104.17 mask 255.255.255.240"""
    user = "admin"
    password = getpass.getpass()
    host = "172.31.104.4"
    interface = "g0/1"
    ip = "172.31.104.17"
    mask = "255.255.255.240"
    session = start_seesion(host, user, password)
    print(config_ip_interface(session, ip, mask, interface).decode('ascii'))

main()

