#!/bin/bash

python3 -m venv env
. env/bin/activate
python3 -m pip install -r requirements.txt
flask --app main run --host=0.0.0.0
