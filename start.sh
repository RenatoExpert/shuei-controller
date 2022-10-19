#!/bin/bash

cd /bin/janus-controller
echo 'Self update'
git pull
echo 'Asuring virtual enviroment'		&& \
python3 -m venv env				&& \
echo 'Activating virtual enviroment'		&& \
. env/bin/activate				&& \
echo 'Installing dependencies'			&& \
python3 -m pip install -r \
	/bin/janus-controller/requirements.txt	&& \
flask --app januspi run --host=0.0.0.0
