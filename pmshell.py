#!/usr/bin/python3
#
# cisco_cmd.py
# Opengear Solutions Engineering, 8 Feb 2022
#  
# SLE-157
# Send a command to a Cisco IOS device through OM pmshell
# Validated on IOS XE version 16.12.04 and IOS version 15.2(7)E4

from netmiko import ConnectHandler, redispatch
import getpass
import time
import inventory
import os

def connect():

    device1 = {
        'host': '10.0.0.4', #change to OM's IP
        'username': 'root',
        'password': 'Op3ng3ar!',
        'device_type': 'terminal_server',
        'session_log': 'cmd_log.txt'
    }   

    conn = ConnectHandler(**device1)

    return conn


def command(port,input):

    conn = connect()

    conn.send_command_timing(f'pmshell -l /dev/{port}')
    conn.write_channel('\r\n\r\n\r\n')
    time.sleep(1)
    conn.write_channel('\r\n\r\n')

    redispatch(conn, device_type='cisco_ios')
    conn.find_prompt()

    conn.enable()  
    output = conn.send_command(input)

    conn.write_channel('\r\n')
    time.sleep(1)

    conn.disconnect()

    # Create and open a temp file to write console output 
    with open("tempFile.txt", "w+") as f:
        f.write(output)
        
    # Read file contents to a var
    with open("tempFile.txt", "r") as g:
        h = g.read()
        print(h)

    # Delete temp file
        os.remove("tempFile.txt")

    return h


if __name__ == "__main__":
    command()