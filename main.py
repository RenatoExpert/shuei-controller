#!/bin/python3

from flask import Flask

#   Serves the web-interface
app = Flask(__name__)
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

#   "Lib": Functions that controls the GPIO

#   Handler between Client and GPIO

#   Slave mode (comunicates to another janus controller)

