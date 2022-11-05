import socket, os, time, json, subprocess, sys

#   Server
port = 2000
host = 'shuei.shogunautomacao.com.br'
server = None # This is a rebuildable socket
#host = 'localhost'

#   Get uuid
if '--fakegpio' in sys.argv:
    def get_uuid():
        return 'fakegadget'
else:
    def get_uuid():
        cpuinfo = open("/proc/cpuinfo", "r")
        for line in cpuinfo:
            if 'Serial' in line:
                return line.split(' ')[-1].split("\n")[0]
                cpuinfo.close()
                break
uuid = get_uuid()

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
        self.setup()
    def setup(self):
        GPIO.setup(self.rp, GPIO.IN)
        GPIO.setup(self.wp, GPIO.OUT)
        GPIO.output(self.wp, GPIO.LOW)

pairs = [
    pair(2, 3),
    pair(23, 24),
    pair(5, 6)
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

def get_gpio_status():
    gpio_status = ''
    for pair in pairs:
        agregate = 0 if GPIO.input(pair.rp) == GPIO.HIGH else 2
        agregate += 2 if GPIO.input(pair.wp) == GPIO.HIGH else 0
        gpio_status += f'{agregate}'
    return gpio_status 

def update_status():
    global server
    gpio_status = get_gpio_status()
    status_send = json.dumps({ 
        "gpio_status": gpio_status
    })
    server.send(bytes(status_send+"\n", 'UTF-8'))

def sync():
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host,port))
    print('Connected')
    hello_send = json.dumps({ 
        "type": "controller",
        "uuid": uuid
    })
    server.send(bytes(hello_send+"\n", 'UTF-8'))
    update_status()
    while True:
        recpak = server.recv(1024)
        command = json.loads(recpak)
        print(f'Received from server {command}')
        if 'args' in command.keys():
            args = command['args']
            if 'pair_id' in args.keys():
                pair_id = int(args['pair_id'])
        if 'cmd' in command.keys():
            cmd = command['cmd']
            if cmd == 'reboot':
                pass
            elif cmd == 'reload':
                pass
            elif cmd == 'upgrade':
                pass
            elif cmd == 'setstate':
                pass
            elif cmd == 'revertstate':
                wpin = pairs[pair_id].wp
                reverse = GPIO.HIGH if GPIO.input(wpin) == GPIO.LOW else GPIO.LOW
                GPIO.output(wpin, reverse)
            elif cmd == 'rest':
                pass
            else:
                raise Exception(f"Unknow command {data}")
                server.close()
                break
        print('Done with success, updating gpio_status')
        update_status()


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


