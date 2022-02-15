from netmikolab import *

device_ip = "172.31.104.4"
username = "admin"
#key_file = "rsa2"
key_file="C:\\Users\\Jack\\Documents\\NPA\\rsa2"

def test_ip_route():
    assert getIPRoute(device_params, "management", "include ^C").split("\n")[1] == "C        172.31.104.0/28 is directly connected, GigabitEthernet0/0"

device_params = {"device_type": "cisco_ios",
                "ip": device_ip,
                "username": username,
                "use_keys": True,
                "key_file": key_file
                }