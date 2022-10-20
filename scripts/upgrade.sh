#!/bin/bash
cd /bin/janus-controller
git pull --rebase
cp systemd/janusd.service /etc/systemd/system
