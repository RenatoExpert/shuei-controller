#!/bin/bash
cd /bin/shuei-controller
git pull --rebase
cp -v systemd/shueid.service /etc/systemd/system
