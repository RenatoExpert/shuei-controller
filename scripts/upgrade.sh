#!/bin/bash
cd /bin/janus-controller
git pull --rebase
cp -v systemd/janusd.service /etc/systemd/system
