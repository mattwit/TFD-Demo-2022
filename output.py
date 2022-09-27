from flask import Flask, render_template, redirect
import os
import subprocess
import sys

app = Flask(__name__)

# @app.route("/")

# def hello():
#     output = os.system("echo hello everybody")
#     print(output, flush=True)
#     return render_template("output.html")
    

@app.route('/', methods=["GET", "POST"])

def openFile():

    # Create and open a temp file to write console output 
    with open("file.txt", "w+") as f:
        output = os.popen("route print").read()
        f.write(output)
    
    # Read file contents to a var
    with open("file.txt", "r") as g:
        h = g.read()
        print(h)

    # Delete temp file
    os.remove("file.txt")

    # Render file contents into page
    # 
    #        
    return render_template('output.html', h=h)



if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=5000)