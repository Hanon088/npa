import re
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
    int_ip = re.search("\d+\.\d+\.\d+\.\d+", result).group()
    int_mask = re.search("/\d+$", result)
    if int_mask:
        int_mask = int_mask.group()
    if includeMask:
        return [int_ip, int_mask]
    return int_ip


def getAllIPInterface(params, includeNonPhysical=True):
    """Get all ip addresses of a device"""
    command = f"sh ip interface br"
    result = getDataFromDevice(params , command)
    result = result.split("\n")[1:]
    ipDict = {}
    for line in result:
        line = line.split()[:2]
        if "Ethernet" not in line[0] and "Serial" not in line[0] and not includeNonPhysical:
            continue
        ipDict.update({line[0]: line[1]})
    return ipDict

def getInterfaceDescriptions(params):
    """Get descriptions of all physical interfaces of a device"""
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
            list_of_des.append(["G" + line[0][2:], description])
        elif len(line) >= 5 and line[0][0] == "G":
            description = ""
            for text in line[3:]:
                description += text + " "
            list_of_des.append(["G" + line[0][2:], description])
        else:
            pass
    return list_of_des

def setInterfaceDescriptions(params):
    """Set descriptions of all physical interfaces of a device"""
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

        if params["ip"] == "172.31.104.6":
            ssh.send_config_set(["interface g0/2","des Connected to WAN"])
        result = ssh.send_command("show int description")
    #maybe find out what to return
    return output

def getipstatus(device_params, interface="all"):
    command = "sh ip int | include line proto"
    output = []
    if interface.find("G") != -1:
        command = "show ip interface " + interface + " | include Gigabit"
    with ConnectHandler(**device_params) as ssh:
        result = ssh.send_command(command)
    result = result.split("\n")
    for line in result:
        line = line.split(" ")
        line_status = line[len(line) - 5][:-1]
        if line[2].find("admin") != -1:
            line_status = "administratively " + line_status
        if line[0].find("L") == -1:
            output.append([line[0][0] + line[0][-3:], line_status, line[len(line) - 1]])
    return output
    
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
                    