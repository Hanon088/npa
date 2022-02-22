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

@pytest.mark.interface
def test_ip_interface():
    ipaddress_r1 = [["G0/0", "172.31.104.4"], ["G0/1", "172.31.104.17"], ["G0/2", "172.31.104.33"], ["G0/3", "unassigned"]]
    ipaddress_r2 = ["G0/0 172.31.104.5", "G0/1 172.31.104.34", "G0/2 172.31.104.49", "G0/3 unassigned"]
    ipaddress_r3 = ["G0/0 172.31.104.6", "G0/1 172.31.104.50", "G0/2 192.168.122.206", "G0/3 unassigned"]
    for interface, ipAddress in ipaddress_r1:
        assert getIP(device_params, interface, includeMask=False) == ipAddress
    #device_params.update({"ip":"172.31.104.5"})

@pytest.mark.subnetmask
def test_subnet_mask():
    assert getIP(device_params, "G0/0")[1] == "/28"
    

@pytest.mark.description
def test_interface_description():
    description_r1 = ["G0/0 Connected to G0/2 of S0 ","G0/1 Connected to G0/2 of S1 ", "G0/2 Connected to G0/1 of R2 ", "G0/3 Not Use "]
    setipdes_all(device_params)
    assert getIPinterfaceDes(device_params , "G") == description_r1
    device_params.update({"ip":"172.31.104.5"})
    setipdes_all(device_params)
    description_r2 = ["G0/0 Connected to G0/3 of S0 ","G0/1 Connected to G0/2 of R1 ", "G0/2 Connected to G0/1 of R3 ", "G0/3 Not Use "]
    assert getIPinterfaceDes(device_params , "G") == description_r2
    device_params.update({"ip":"172.31.104.6"})
    setipdes_all(device_params)
    description_r2 = ["G0/0 Connected to G1/0 of S0 ","G0/1 Connected to G0/2 of R2 ", "G0/2 Connected to Nat ", "G0/3 Not Use "]
    assert getIPinterfaceDes(device_params , "G") == description_r2

def test_ip_route():
    managementRoute = ['C        172.31.104.0/28 is directly connected, GigabitEthernet0/0']
    assert getIPRoute(device_params, "management", "include ^C") == managementRoute
    controlDataRoute = ['C        172.31.104.16/28 is directly connected, GigabitEthernet0/1',
                        'C        172.31.104.32/28 is directly connected, GigabitEthernet0/2']
    assert getIPRoute(device_params, "control-Data", "include ^C") == controlDataRoute




                