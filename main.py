from flask import Flask, render_template
import socket

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

