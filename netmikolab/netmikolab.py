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
        if not bool(re.search("Ethernet|Serial", line)) and not includeNonPhysical:
            continue
        line = line.split()[:2]
        ipDict.update({line[0]: line[1]})
    return ipDict


def getInterfaceDescriptions(params):
    """Get descriptions of all physical interfaces of a device"""
    command = f"show int description"
    raw_text = getDataFromDevice(params, command)
    raw_text = raw_text.split("\n")        
    output = []
    for line in raw_text:
        list_ram = []
        re_interface = re.search('Gi[0-9]/[0-9]', line)
        re_des = re.search('Not Use|Connected \S+ \S+ \S+ \S+|Connected to WAN', line)
        if re_interface != None and re_des != None:
            list_ram.append("G" + re_interface.group()[-3:])
            list_ram.append(re_des.group())
            output.append(list_ram)
    return output

def setInterfaceDescriptions(params):
    """Set descriptions of all physical interfaces of a device"""
    result = getDataFromDevice(params, "sh cdp nei")
    ipDict = getAllIPInterface(params, False)
    intStatus = {}
    for intName, intIp in ipDict.items():
        intName = intName.split("Ethernet")
        intStatus.update({intName[0][0] + intName[1]: intIp != "unassigned"})

    result = re.search("Device ID[\w\s\S]*Total cdp", result).group().split("\n")[1:-2]
    descDict = {}
    for line in result:
        connectedDevice = re.search("\S+\d+", line).group()
        localInterface =  re.search("[A-Z][a-z][a-z] \d/\d", line).group()
        localInterface = localInterface[0] + localInterface[4:]
        connectedPort =  re.search("[A-Z][a-z][a-z] \d/\d$", line).group()
        connectedPort = connectedPort[0] + connectedPort[4:]
        descDict.update({str(localInterface): f"Connected to {connectedPort} of {connectedDevice}"})

    with ConnectHandler(**params) as ssh:
        for interface in intStatus:
            if intStatus[interface]:
                ssh.send_config_set(["Interface " + interface,"des " + descDict[interface]])
            else:
                ssh.send_config_set(["Interface " + interface,"des Not Use"])

        if params["ip"] == "172.31.104.6":
            ssh.send_config_set(["interface g0/2","des Connected to WAN"])
        result = ssh.send_command("show int description")
    #maybe find out what to return
    return descDict

def getipstatus(params, interface="all"):
    command = "sh ip int | include line proto"
    output = []
    if interface.find("G") != -1:
        command = "show ip interface " + interface + " | include Gigabit"
    with ConnectHandler(**params) as ssh:
        result = ssh.send_command(command)
    result = result.split("\n")
    print(result)
    for line in result:
        re_interface = re.search('GigabitEthernet\d/\d', line)
        re_py_status = re.search('is \S+', line)
        re_protocol_status = re.search('protocol is \S+', line)
        if re_interface != None and re_py_status != None and re_protocol_status != None:
            list_ram_1 = []
            list_ram_1.append(re_interface.group()[0] + re_interface.group()[-3:])
            if re_py_status.group()[3:] == "administratively":
                list_ram_1.append(re_py_status.group()[3:] + " down")
            else:
                list_ram_1.append(re_py_status.group()[3:-1])
            list_ram_1.append(re_protocol_status.group()[12:])
            output.append(list_ram_1)
    return output
    
if __name__ == '__main__':
    device_ip = "172.31.104.6"
    username = "admin"
    key_file = "rsa2"
    # key_file="C:\\Users\\Jack\\Documents\\NPA\\rsa2"

    device_params = {"device_type": "cisco_ios",
                    "ip": device_ip,
                    "username": username,
                    "use_keys": True,
                    "key_file": key_file
                    }
