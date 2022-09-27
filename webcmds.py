#!/usr/bin/python3
#

from netmiko import ConnectHandler
from flask import Flask, render_template, request
import os
import inventory
from pmshell import command
from iperf import iperfCmd


app = Flask(__name__)

hosts = inventory.hosts
commands = inventory.iosCommands
serialPorts = inventory.serialPorts

# netmiko connection function
def connect(host):

    device1 = {
        'host': host,
        'username': inventory.username,
        'password': inventory.pword,
        'device_type': 'cisco_ios',
        'session_log': 'cmd_log.txt'
    }

    conn = ConnectHandler(**device1)

    return conn

def junosConnect(host):

    device1 = {
        'host': '10.0.0.1',
        'username': inventory.juser,
        'password': inventory.jpword,
        'device_type': 'junos',
        'session_log': 'cmd_log.txt'
    }      

    conn = ConnectHandler(**device1)

    return conn


# start page
@app.route('/', methods=["GET", "POST"])
def index():

    return render_template('index.html')

# select priv exec command
@app.route('/selectcmd', methods=["GET", "POST"])
def selectcmd():

    if request.method == 'POST':

        host = request.form.get("device")
        input = request.form.get("selcmd")

        # check for user input
        if not host or not input:
            return render_template('oops.html')
        else:
            # pass host & input to cmdOutput function
            h = privExecOutput(host,input)
            
            # Render file contents into output page  
            return render_template('output.html', h=h, host=host, input=input)

    return render_template('selectcmd.html', hosts=hosts)

# select command via serial
@app.route('/serialcmd', methods=["GET", "POST"])
def serialcmd():

    if request.method == 'POST':

        port = request.form.get("device")
        input = request.form.get("selcmd")

        # check for user input
        if not port or not input:
            return render_template('oops.html')
        else:
            # pass host & input to cmdOutput function
            h = command(port,input)
            
            # Render file contents into output page  
            return render_template('output.html', h=h, port=port, input=input)


    return render_template('serialcmd.html', serialPorts=serialPorts)

# enter priv exec command
@app.route('/entercmd', methods=["GET", "POST"])
def entercmd():

    if request.method == 'POST':

        host = request.form.get("device")
        input = request.form.get("textcmd")

        # check for user input
        if not host or not input:
            return render_template('oops.html')
        else:
            # pass host & input to cmdOutput function
            h = privExecOutput(host,input)
            
            # Render file contents into output page  
            return render_template('output.html', h=h, host=host, input=input)

    return render_template('entercmd.html', hosts=hosts)

@app.route('/junoscmd', methods=["GET", "POST"])
def junosCmd():

    if request.method == 'POST':

        host = request.form.get("device")
        input = request.form.get("selcmd")

        # check for user input
        if not host or not input:
            return render_template('oops.html')
        else:
            # pass host & input to cmdOutput function
            h = privExecOutput(host,input)
            
            # Render file contents into output page  
            return render_template('output.html', h=h, host=host, input=input)

    return render_template('selectcmd.html', hosts=hosts)


# enter global config commands
# enter command
@app.route('/configcmd', methods=["GET", "POST"])
def configcmd():

    if request.method == 'POST':

        host = request.form.get("device")
        input = request.form.get("textcmd")

        # check for user input
        if not host or not input:
            return render_template('oops.html')
        else:
            # pass host & input to cmdOutput function
            h = globalConfOutput(host,input)
            
            # Render file contents into output page  
            return render_template('output.html', h=h, host=host, input=input)

    return render_template('configcmd.html', hosts=hosts)

@app.route('/iperf', methods=["GET", "POST"])
def iperf():

    if request.method == 'POST':

        h = iperfCmd()

        return render_template('iperfoutput.html', h=h)

    return render_template('iperf.html')


# command functions below
#
# connect and execute priv exec cli command 
def privExecOutput(host,input):

    # establish ssh session
    # pass host to connect function
    conn = connect(host)
    
    # send command to device
    output = conn.send_command(input)

    # disconnect from device
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

# connect and execute priv exec cli command 
def globalConfOutput(host,input):

    # establish ssh session
    # pass host to connect function
    conn = connect(host)
    
    # send command to device
    output = conn.send_config_set(input)

    # disconnect from device
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


# connect and execute priv exec cli command 
def junosOutput(host,input):

    # establish ssh session
    # pass host to connect function
    conn = junosConnect(host)
    
    # send command to device
    output = conn.send_config_set(input)

    # disconnect from device
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
    
    app.run(host="0.0.0.0", port=5000)