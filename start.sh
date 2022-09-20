#!/bin/bash

. env/bin/activate
python3 -m pip install -r requirements.txt
flask --app main run --host=0.0.0.0
