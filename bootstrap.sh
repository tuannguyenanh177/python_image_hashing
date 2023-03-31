#!/bin/sh
export FLASK_APP=./image_hashing/index.py
pipenv run flask --debug run -h 0.0.0.0 -p 5001