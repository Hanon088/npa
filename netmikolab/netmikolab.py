from cProfile import run
import re
from turtle import st
from netmiko import ConnectHandler

def getDataFromDevice(params, command):
    """Send command to device and return the result"""
    with ConnectHandler(**params) as ssh:
        result = ssh.send_command(command)
        return result

def getIPRoute(params, vrf="", pipe=""):
    """Get routing table from device"""
    command = f"sh ip route{' vrf '*(vrf != '') + vrf}{' | '*(pipe != '') + pipe}"
    result = getDataFromDevice(params, command)
    result = result.split("\n")
    #Adding .index incase console loggin changed the output
    result = result[result.index('Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP') + 1:]
    return result

def getIPInterface(params, interface):
    command = f"sh ip interface br"
    result = getDataFromDevice(params , command)
    result = result.split("\n")
    list_of_ip = []
    for line in result[1:]:
        line = line.split()
        if line[0].find("Gigabit") != -1:
            line[0] = "G" + line[0][15:]
        list_of_ip.append(line[0:2])
    result = []
    for interface_in in list_of_ip:
        if interface == "G" and interface_in[0].find("G") != -1:
            string_out = interface_in[0] + " " + interface_in[1]
            result.append(string_out)
    return result

if __name__ == '__main__':
    device_ip = "172.31.104.4"
    username = "admin"
    key_file = "rsa2"
    # key_file="C:\\Users\\Jack\\Documents\\NPA\\rsa2"

    device_params = {"device_type": "cisco_ios",
                    "ip": device_ip,
                    "username": username,
                    "use_keys": True,
                    "key_file": key_file
                    }
    # print(getIPRoute(device_params, "management", "include ^C"))
    # print(getIPRoute(device_params, "control-Data", "include ^C"))
    # print(getIPInterface(device_params, "G"))

