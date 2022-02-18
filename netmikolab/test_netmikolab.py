import pytest
from netmikolab import *

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

def test_ip_interface():
    ipaddress_r1 = ["G0/0 172.31.104.4", "G0/1 172.31.104.17", "G0/2 172.31.104.33", "G0/3 unassigned"]
    ipaddress_r2 = ["G0/0 172.31.104.5", "G0/1 172.31.104.34", "G0/2 172.31.104.49", "G0/3 unassigned"]
    assert getIPInterface(device_params, "G") == ipaddress_r1
    device_params.update({"ip":"172.31.104.5"})
    assert getIPInterface(device_params, "G") == ipaddress_r2

def test_ip_route():
    managementRoute = ['C        172.31.104.0/28 is directly connected, GigabitEthernet0/0']
    assert getIPRoute(device_params, "management", "include ^C") == managementRoute

    controlDataRoute = ['C        172.31.104.16/28 is directly connected, GigabitEthernet0/1',
                        'C        172.31.104.32/28 is directly connected, GigabitEthernet0/2']
    assert getIPRoute(device_params, "control-Data", "include ^C") == controlDataRoute




                