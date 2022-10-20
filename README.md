# Janus Core
## Setup a new device
1.	Download ISO from https://
2.	Copy the content to a storage device (SD card is prefered)
	Rufus(windows) or dd(gnu) may be useful
3.	Turn on Janus Device
4.	Connect to SSID "Janus Controller" wireless network
5.	Open your browser at '192.168.0.1'
6.	A setup screen is going to appear
7.	Set your wireless network
8.	Choose an operation mode (Master or slave).
	In case of slave mode, point its master address
9.	Save and Reset

## Install on raspberry pi
Copy and paste on terminal
```
https://raw.githubusercontent.com/RenatoExpert/janus-controller/main/install.sh | sh
```

## API - Control it with POST http requests
Command		|Request		| Description
:--------:	|:-----------		| :----------
reboot		| /reboot		| Reboot Device
reload		| /reload		| Restart Janus Daemon
upgrade		| /upgrade		| Upgrade Daemon Version
getstate	| /getstate?gpio=N	| Returns status from a GPIO pin
setstate	| /setstate?gpio=N	| Set GPIO pin as HIGH or LOW


