# import pexpect
import pexpect
""" pexpect lab for config R1 R2 R3 looback ip"""
Prompt = "#"
Username = "admin"
Password = "cisco"
IP = "10.0.15.104"
Command = "show ip interface br"
"""pexpect.spawn not support in window"""
child = pexpect.popen_spawn.PopenSpawn('telnet'+ IP)
child.expect('Username')
child.sendline(Username)
child.expect('Password')
child.sendline(Password)
child.expect(Prompt)
child.sendline(Command)
child.expect(Prompt)
result = child.before
print(result)
print()
print(result.decode('UTF-8'))
