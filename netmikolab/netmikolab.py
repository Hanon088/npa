import re
from turtle import down
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

def getIP(params, interface, includeMask=True):
    """Get ip address of an interface"""
    command = f"sh ip int {interface.lower()} | include Internet address"
    result = getDataFromDevice(params, command)
    if result == "":
        return "unassigned"
    result = result.split("is ")[1]
    result = result.split("/")
    int_ip = result[0]
    int_mask = "/" + result[1]
    if includeMask:
        return [int_ip, int_mask]
    return int_ip


def getAllIPInterface(params, includeLoopback=True):
    """Get all ip addresses of a device"""
    command = f"sh ip interface br"
    result = getDataFromDevice(params , command)
    result = result.split("\n")[1:]
    """list_of_ip = []
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
    return list_of_ip"""
    ipDict = {}
    for line in result:
        line = line.split()[:2]
        if "Loopback" in line[0] and not includeLoopback:
            continue
        ipDict.update({line[0]: line[1]})
    return ipDict

def getIPinterfaceDes(params, interface):
    command = f"show int description"
    result = getDataFromDevice(params, command)
    result = result.split("\n")
    list_of_des = []
    for line in result[1:]:
        line = line.split()
        if line[1] == "admin" and len(line) >= 5 and line[0][0] == "G":
            description = ""
            for text in line[4:]:
                description += text + " "
            list_of_des.append("G" + line[0][2:] + " " + description)
        elif len(line) >= 5 and line[0][0] == "G":
            description = ""
            for text in line[3:]:
                description += text + " "
            list_of_des.append("G" + line[0][2:] + " " + description)
        else:
            pass
    return list_of_des

def setipdes_all(params):
    result = getDataFromDevice(params, "sh cdp nei")
    ipDict = getAllIPInterface(params, False)
    intStatus = {}
    for intName, intIp in ipDict.items():
        intName = intName.split("Ethernet")
        intStatus.update({intName[0][0] + intName[1]: intIp != "unassigned"})

    result = result.split("\n")
    result_len = len(result)
    result = result[5:result_len-2]
    output = {}
    for line in result:
        result = line.split()
        line = result[:1]
        line[0] = line[0][:2]
        line_len = len(result)
        line.append(result[1:3])
        line[1] = line[1][0][0] + line[1][1]
        line.append(result[line_len-2:line_len])
        line[2] = line[2][0][0] + line[2][1]
        output.update({line[1]:"Connected to " + line[2] + " of " + line[0]})

    with ConnectHandler(**params) as ssh:
        for interface in intStatus:
            if intStatus[interface]:
                ssh.send_config_set(["Interface " + interface,"des " + output[interface]])
            else:
                ssh.send_config_set(["Interface " + interface,"des Not Use"])

        if params["ip"] == "172.31.104.6" and interface == "G0/2":
            ssh.send_config_set(["interface g0/2","des Connected to Nat"])
        result = ssh.send_command("show int description")
    #maybe find out what to return
    return output

if __name__ == '__main__':
    device_ip = "172.31.104.4"
    username = "admin"
    #key_file = "rsa2"
    key_file="C:\\Users\\Jack\\Documents\\NPA\\rsa2"

    device_params = {"device_type": "cisco_ios",
                    "ip": device_ip,
                    "username": username,
                    "use_keys": True,
                    "key_file": key_file
                    }
    # print(getIPRoute(device_params, "management", "include ^C"))
    # print(getIPRoute(device_params, "control-Data", "include ^C"))
    # print(getIP(device_params, "G0/0"))
    # print(getIP(device_params, "G0/0", False))
    # print(getIP(device_params, "G0/3"))
    # print(getIPinterfaceDes(device_params, "G"))
    #print(getAllIPInterface(device_params))
    #print(getAllIPInterface(device_params, False))
    print(setipdes_all(device_params))
