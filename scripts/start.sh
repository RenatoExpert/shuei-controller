#!/bin/bash

cd /bin/shuei-controller
echo 'Self update'
./scripts/upgrade.sh 
echo 'Asuring virtual enviroment'		&& \
python3 -m venv env				&& \
echo 'Activating virtual enviroment'		&& \
. env/bin/activate				&& \
echo 'Installing dependencies'			&& \
python3 -m pip install -r \
	/bin/shuei-controller/requirements.txt	&& \
shuei
