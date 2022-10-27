#import RPi.GPIO as GPIO
import socket
import os
import time
#from PyAccessPoint import pyaccesspoint

#   First use: make wireless hotspot
#access_point = pyaccesspoint.AccessPoint(wlan='wlan1', ssid='Janus')
#access_point.start()
#access_point.is_running()
# access_point.stop()

"""
#   Setting GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.IN)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(23,GPIO.IN)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(5,GPIO.IN)
GPIO.setup(6,GPIO.OUT)
"""

#   Get uuid
def get_uuid():
    os.system("grep /proc/cpuinfo 'Serial'")

#   Upgrade
def upgrade():
    command = os.system(". /bin/shuei-controller/scripts/upgrade")
    return str(command)

#   Serves the web-interface

#   Keep synchronizing with Server
port = 2000
host = 'localhost'
def sync():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    s.send(b'{ "uuid":"j324u", "gstatus":"333" }\n')
    data = s.recv(1024)
    s.send(b'0')
    s.close()
    print('Server', repr(data))

if __name__ == "__main__":
    while True:
        try:
            sync()
        except ConnectionRefusedError:
            print("Connection refused, trying again...")
        except:
            print("Unknown error")
        finally:
            time.sleep(1)


