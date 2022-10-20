from flask import Flask, render_template
import RPi.GPIO as GPIO
import socket
import os
#from PyAccessPoint import pyaccesspoint

#   First use: make wireless hotspot
#access_point = pyaccesspoint.AccessPoint(wlan='wlan1', ssid='Janus')
#access_point.start()
#access_point.is_running()
# access_point.stop()

#   Setting GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.IN)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(23,GPIO.IN)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(5,GPIO.IN)
GPIO.setup(6,GPIO.OUT)

#   Upgrade
def upgrade():
    command = os.system("./bin/janus-controller/scripts/upgrade")
    return str(command)

#   Serves the web-interface
def create_app (test_config=None):
    app = Flask(__name__, template_folder='web', instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass


    @app.route("/")
    def home_page():
        return render_template('index.html')

    @app.route("/its_ip")
    def its_ip():
        return socket.gethostbyname(socket.gethostname())

    #   As defined

    @app.route("/reboot")
    def reboot():
        return os.system("reboot")

    @app.route("/reload")
    def reload():
        return "It may reset janus daemon"

    @app.route("/upgrade")
    def upgrade():
        return upgrade()

    @app.route("/getstate/<int:pin>")
    def getstate(pin):
        return str(GPIO.input(pin))

    @app.route("/setstate/<int:pin>/<int:bool_value>")
    def setstate(pin, bool_value):
        value = GPIO.HIGH if bool_value==1 else GPIO.LOW
        return str(GPIO.output(pin, value))


    from . import db
    db.init_app(app)

    return app

#   "Lib": Functions that controls the GPIO

#   Handler between Client and GPIO

#   Slave mode (comunicates to another janus controller)

