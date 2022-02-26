import pytest
from netmikolab import *

router1 = { "management_ip": "172.31.104.4",
            "interfaces": [
                             ["G0/0", "172.31.104.4", "/28"],
                             ["G0/1", "172.31.104.17", "/28"],
                             ["G0/2", "172.31.104.33", "/28"],
                             ["G0/3", "unassigned"]
                             ],
            "interface_description": [
                                      ["G0/0", "Connected to G0/2 of S0"],
                                      ["G0/1", "Connected to G0/2 of S1"],
                                      ["G0/2", "Connected to G0/1 of R2"],
                                      ["G0/3", "Not Use"]
                                      ],
            "interface_status" : [
                                    ["G0/0", "up", "up"],
                                    ["G0/1", "up", "up"],
                                    ["G0/2", "up", "up"],
                                    ["G0/3", "administratively down", "down"],
                                    ],
            "management_route": ['C        172.31.104.0/28 is directly connected, GigabitEthernet0/0'],
            "control_data_route": ['C        172.31.104.16/28 is directly connected, GigabitEthernet0/1',
                                   'C        172.31.104.32/28 is directly connected, GigabitEthernet0/2']
            }

router2 = { "management_ip": "172.31.104.5",
            "interfaces": [
                             ["G0/0", "172.31.104.5", "/28"],
                             ["G0/1", "172.31.104.34", "/28"],
                             ["G0/2", "172.31.104.49", "/28"],
                             ["G0/3", "unassigned"]
                             ],
            "interface_description": [
                                      ["G0/0", "Connected to G0/3 of S0"],
                                      ["G0/1", "Connected to G0/2 of R1"],
                                      ["G0/2", "Connected to G0/1 of R3"],
                                      ["G0/3", "Not Use"]
                                      ],
            "interface_status" : [
                                    ["G0/0", "up", "up"],
                                    ["G0/1", "up", "up"],
                                    ["G0/2", "up", "up"],
                                    ["G0/3", "administratively down", "down"],
                                    ],
            "management_route": ['C        172.31.104.0/28 is directly connected, GigabitEthernet0/0'],
            "control_data_route": ['C        172.31.104.32/28 is directly connected, GigabitEthernet0/1',
                                   'C        172.31.104.48/28 is directly connected, GigabitEthernet0/2']
            }

router3 = { "management_ip": "172.31.104.6",
            "interfaces": [
                             ["G0/0", "172.31.104.6", "/28"],
                             ["G0/1", "172.31.104.50", "/28"],
                             ["G0/3", "unassigned"]
                             ],
            "interface_description": [
                                      ["G0/0", "Connected to G1/0 of S0"],
                                      ["G0/1", "Connected to G0/2 of R2"],
                                      ["G0/2", "Connected to WAN"],
                                      ["G0/3", "Not Use"]
                                      ],
            "interface_status" : [
                                    ["G0/0", "up", "up"],
                                    ["G0/1", "up", "up"],
                                    ["G0/2", "up", "up"],
                                    ["G0/3", "administratively down", "down"],
                                    ],
            "management_route": ['C        172.31.104.0/28 is directly connected, GigabitEthernet0/0'],
            "control_data_route": ['C        172.31.104.48/28 is directly connected, GigabitEthernet0/1',
                                   'C        192.168.122.0/24 is directly connected, GigabitEthernet0/2']
            }

username = "admin"
key_file = "rsa2"
# key_file="C:\\Users\\Jack\\Documents\\NPA\\rsa2"
device_params = {"device_type": "cisco_ios",
                "ip": "",
                "username": username,
                "use_keys": True,
                "key_file": key_file
                }

def test_r1():
    router = router1
    device_params.update({"ip": router["management_ip"]})

    #ip address
    for interface in router["interfaces"]:
        intName = interface[0]
        if "unassigned" in interface:
            assert getIP(device_params, intName) == "unassigned"
        else:
            address = interface[1]
            mask = interface[2]
            assert getIP(device_params, intName) == [address, mask]

    #test interface status
    assert getipstatus(device_params) == router["interface_status"]
    
    #ip route
    assert getIPRoute(device_params, "management", "include ^C") == router["management_route"]
    assert getIPRoute(device_params, "control-Data", "include ^C") == router["control_data_route"]

    #interface description
    setInterfaceDescriptions(device_params)
    assert getInterfaceDescriptions(device_params) == router["interface_description"]

def test_r2():
    router = router2
    device_params.update({"ip": router["management_ip"]})

    #ip address
    for interface in router["interfaces"]:
        intName = interface[0]
        if "unassigned" in interface:
            assert getIP(device_params, intName) == "unassigned"
        else:
            address = interface[1]
            mask = interface[2]
            assert getIP(device_params, intName) == [address, mask]

    #test interface status
    assert getipstatus(device_params) == router["interface_status"]
    
    #ip route
    assert getIPRoute(device_params, "management", "include ^C") == router["management_route"]
    assert getIPRoute(device_params, "control-Data", "include ^C") == router["control_data_route"]

    #interface description
    setInterfaceDescriptions(device_params)
    assert getInterfaceDescriptions(device_params) == router["interface_description"]

def test_r3():
    router = router3
    device_params.update({"ip": router["management_ip"]})

    #ip address
    for interface in router["interfaces"]:
        intName = interface[0]
        if "unassigned" in interface:
            assert getIP(device_params, intName) == "unassigned"
        else:
            address = interface[1]
            mask = interface[2]
            assert getIP(device_params, intName) == [address, mask]
    #test interface status
    assert getipstatus(device_params) == router["interface_status"]
    
    #ip route
    assert getIPRoute(device_params, "management", "include ^C") == router["management_route"]
    assert getIPRoute(device_params, "control-Data", "include ^C") == router["control_data_route"]

    #interface description
    setInterfaceDescriptions(device_params)
    assert getInterfaceDescriptions(device_params) == router["interface_description"]
