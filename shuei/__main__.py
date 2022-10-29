import socket
import os
import time
import json
import subprocess
import sys

#   Server
port = 2000
host = 'shuei.shogunautomacao.com.br'
#host = 'localhost'

#   GPIO
if '--fakegpio' in sys.argv:
    from fakegpio import GPIO
else:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)

class pair:
    def __init__(self, rp, wp):
        self.rp = rp
        self.wp = wp
        GPIO.setup(rp, GPIO.IN)
        GPIO.setup(wp, GPIO.OUT)

pairs = [
    pair(2,3),
    pair(23,24),
    pair(5,6)
]

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
    for pair in pairs:
        agregate = 1 if GPIO.input(pair.rp) else 0
        agregate += 2 if GPIO.input(pair.wp) else 0
        gstatus += f'{agregate}'
    return gstatus 

def sync():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    gstatus = get_gstatus()
    server = s.connect((host,port))
    status_send = json.dumps({ 
        "type":"controller",
        "uuid":"j324u",
        "gstatus":gstatus
    })
    s.send(bytes(status_send+"\n", 'UTF-8'))
    recpak = s.recv(1024)
    command = json.loads(recpak)
    cmd = ''
    args = {}
    pair_id = ''
    if 'args' in command.keys():
        args = command['args']
        if 'pair_id' in args.keys():
            pair_id = int(args['pair_id'])
    if 'cmd' in command.keys():
        cmd = command['cmd']
        match cmd:
            case 'reboot':
                s.send(b'0')
            case 'reload':
                s.send(b'0')
            case 'upgrade':
                s.send(
                    bytes(upgrade()+"\n",'UTF-8')
                )
            case 'setstate':
                s.send(b'0')
            case 'revertstate':
                wpin = pairs[pair_id].wp
                reverse = not GPIO.input(wpin)
                GPIO.output(wpin, reverse)
            case 'rest':
                pass
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


