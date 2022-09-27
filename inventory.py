#!/usr/bin/python3

# device credentials
username = 'ogapp'
pword = 'example_password'

# OM's
om1 = '10.0.0.8'
om2 = '10.0.0.4'

# devices ip or hostname
hosts = [
    '10.0.0.2',
    '10.0.0.3'
]

# pmshell ports
serialPorts = [
    'port21',
    'port23'
]

# list of commands to select
iosCommands = [
    'show ip int brief',
    'show ip route',
    'show lldp neighbor',
    'show run',
    'show version',
    'ping 1.1.1.1'
]