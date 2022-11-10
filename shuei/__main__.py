import socket, os, time, json, subprocess, sys

raw_config = open('config.json', 'r').read()
config = json.loads(raw_config)

#   Server
host = config['host']
port = int(config['port'])
server = None # This is a rebuildable socket

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

gadgets = {
	gconf: {
		'name':gconf,
		'rp':config['gadgets'][gconf]['read'],
		'wp':config['gadgets'][gconf]['write']
	}
	for gconf in config['gadgets']
}

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

def get_status():
	gpio_status = {}
	for gadget in gadgets:
		gpio_status[gadget] = {
			'sensor': str(GPIO.input(gadgets[gadget]['rp'])),
			'relay': str(GPIO.input(gadgets[gadget]['wp'])),
			'mode': str(gadgets[gadget]['mode']),
			'theme': str(gadgets[gadget]['theme'])
		}
	print(gpio_status)
	return gpio_status

def update_status():
	global server
	status_send = json.dumps(get_status())
	print(status_send)
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
                wpin = gadgets[pair_id].wp
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

