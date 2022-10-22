# Shuei Controller 守衛コントローラ
## Setup a new device
1.	Download ISO from https://
2.	Copy the content to a storage device (SD card is prefered)
	Rufus(windows) or dd(gnu) may be useful
3.	Turn on Shuei Device
4.	Connect to SSID "Shuei Controller" wireless network
5.	Open your browser at '192.168.0.1'
6.	A setup screen is going to appear
7.	Set your wireless network
8.	 ~~Choose an operation mode (Master or slave).
	In case of slave mode, point its master address~~ <br>
	Not using master-slave flexible model anymore
9.	Save and Reset

## Install on raspberry pi
Copy and paste on terminal
```
curl https://raw.githubusercontent.com/RenatoExpert/shuei-controller/main/scripts/install.sh | sh
```

## API - Control it with POST http requests
Command		|Request			| Description
:--------:	|:-----------			| :----------
reboot		| /reboot			| Reboot Device
reload		| /reload			| Restart Shuei Daemon
upgrade		| /upgrade			| Upgrade Daemon Version
getstate	| /getstate/gpio\_pin		| Returns status from a GPIO pin
setstate	| /setstate/gpio\_pin/state	| Set GPIO pin with "1" or "0"

## Development progress
- [x] Install with sh
- [x] Response to GET /
- [x] Daemon working
- [x] Start on boot automatically
- [ ] Wifi hotspot on first use
- [x] Self-update from github
- [x] GPIO pins responds to API calls
- [x] GPIO pins reading response using API calls
- [ ] Package .deb
- [ ] Dockerize
- [ ] Read-to-go iso for Raspberry Pi

