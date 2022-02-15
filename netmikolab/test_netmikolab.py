from netmikolab import *

device_ip = "172.31.104.4"
username = "admin"
#key_file = "rsa2"
key_file="C:\\Users\\Jack\\Documents\\NPA\\rsa2"

def test_ip_route():
    managementRoute = ['C        172.31.104.0/28 is directly connected, GigabitEthernet0/0']
    assert getIPRoute(device_params, "management", "include ^C") == managementRoute

    controlDataRoute = ['C        172.31.104.16/28 is directly connected, GigabitEthernet0/1',
                        'C        172.31.104.32/28 is directly connected, GigabitEthernet0/2']
    assert getIPRoute(device_params, "control-Data", "include ^C") == controlDataRoute

device_params = {"device_type": "cisco_ios",
                "ip": device_ip,
                "username": username,
                "use_keys": True,
                "key_file": key_file
                }