# import pexpect
import pexpect
import getpass
import time

""" pexpect lab for config R1 R2 R3 looback ip"""
def start_session(host, Username, Password):
    """start child on pexpect"""
    child = pexpect.spawn('telnet '+ host)
    child.expect('Username')
    child.sendline(Username)
    child.expect('Password')
    child.sendline(Password)
    child.expect("#")
    return child
def set_ip_interface(child, ip, mask, interface):
    """config interface ip and no shutdown interface"""
    child.sendline("config ter")
    time.sleep(1)
    child.expect("#")
    child.sendline("interface " + interface)
    child.expect("#")
    child.sendline("ip address " + ip + " " + mask)
    child.expect("#")
    child.sendline("no shutdown")
    child.expect("#")
    child.sendline("end")
    child.expect("#")
    child.sendline("show ip interface br")
    child.expect("#")
    return child.before.decode('UTF-8')

def main ():
    Username = "admin"
    Password = getpass.getpass()
    list_of_configuration = [{"172.31.104.4":"1.1.1.1"},{"172.31.104.5":"2.2.2.2"},{"172.31.104.6":"3.3.3.3"}]
    for config in list_of_configuration:
        child = start_session(list(config.keys())[0],Username,Password)
        print("config for ip" + list(config.keys())[0])
        print(set_ip_interface(child, list(config.values())[0], "255.255.255.240", "loopback 0"))
    print("end script")
main()