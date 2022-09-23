from flask import Flask, render_template
import socket
from PyAccessPoint import pyaccesspoint

#   First use: make wireless hotspot
def __init__():
    print ('working')
    access_point = pyaccesspoint.AccessPoint(wlan='wlan1', ssid='Janus')
    access_point.start()
    access_point.is_running()
# access_point.stop()

#   Serves the web-interface
app = Flask(__name__, template_folder='web')
@app.route("/")
def home_page():
    return render_template('index.html')

@app.route("/its_ip")
def its_ip():
    return socket.gethostbyname(socket.gethostname())

#   "Lib": Functions that controls the GPIO

#   Handler between Client and GPIO

#   Slave mode (comunicates to another janus controller)

