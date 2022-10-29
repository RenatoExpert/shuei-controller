import socket
import os
import time
import json
import subprocess
import sys

#   Server
port = 2000
host = 'shuei.shogunautomacao.com.br'

#   GPIO
if '--fakegpio' in sys.argv:
    from fakegpio import GPIO
else:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)

readlist= [2, 23, 5]
writelist= [3, 24, 6]

GPIO.setup(2,GPIO.IN)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(23,GPIO.IN)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(5,GPIO.IN)
GPIO.setup(6,GPIO.OUT)

#from PyAccessPoint import pyaccesspoint

#   First use: make wireless hotspot
#access_point = pyaccesspoint.AccessPoint(wlan='wlan1', ssid='Janus')
#access_point.start()
#access_point.is_running()
# access_point.stop()


#   Get uuid
def get_uuid():
    os.system("grep /proc/cpuinfo 'Serial'")

#   Upgrade
def upgrade():
    try:
        proc = subprocess.Popen(
                [".", "/bin/shuei-controller/scripts/upgrade"],
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                text=True
        )
        return str(proc.returncode)
    except Exception as err:
        print('Error here:', err.errno)
        return f'{err.errno}'

def get_gstatus():
    gstatus = ''
    for item in readlist:
        agregate = '1' if GPIO.input(item) else '0'
        gstatus += agregate
    print(gstatus)
    return gstatus 

def sync():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    gstatus = get_gstatus()
    s.connect((host,port))
    print('how', gstatus)
    status_send = json.dumps({ 
        "type":"controller",
        "uuid":"j324u",
        "gstatus":gstatus
    })
    s.send(bytes(status_send, 'UTF-8'))
    command = json.loads(s.recv(1024).decode('UTF-8'))
    print(command)
    cmd = command['cmd']
    print(cmd)
    print('Server:', cmd)
    match cmd:
        case 'reboot':
            s.send(b'0')
        case 'reload':
            s.send(b'0')
        case 'upgrade':
            s.send(
                bytes(upgrade(),'UTF-8')
            )
        case 'setstate':
            s.send(b'0')
        case 'rest':
            s.send(b'0')
        case _:
            raise Exception(f"Unknow command {data}")
    s.close()

if __name__ == "__main__":
    while True:
        try:
            sync()
        except ConnectionRefusedError:
            print("Connection refused, trying again...")
        except Exception as err:
            print("Unknown error", err)
        finally:
            time.sleep(1)


