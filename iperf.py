#!/usr/bin/python3
#

from netmiko import ConnectHandler, redispatch
import inventory
import os
import time

def connect():

    device1 = {
        'host': inventory.om1, #change to OM's IP
        'username': inventory.omuser,
        'password': inventory.ompword,
        'device_type': 'terminal_server',
        'session_log': 'cmd_log.txt'
    }   

    device2 = {
        'host': inventory.om2, #change to OM's IP
        'username': inventory.omuser,
        'password': inventory.ompword,
        'device_type': 'terminal_server',
        'session_log': 'cmd_log.txt'
    }   

    conn1 = ConnectHandler(**device1)
    conn2 = ConnectHandler(**device2)

    return conn2


def iperfCmd():

    conn2 = connect()

    conn2.send_command_timing("cd iperf")

    output = conn2.send_command_timing("./iperf_c.sh")

    conn2.disconnect()

    # Create and open a temp file to write console output 
    with open("tempFile.txt", "w+") as f:
        f.write(output)
        
    # Read file contents to a var
    with open("tempFile.txt", "r") as g:
        h = g.read()
        print(h)

    # Delete temp file
        os.remove("tempFile.txt")

    return output


if __name__ == "__main__":

    # iperfServer()
    iperfCmd()