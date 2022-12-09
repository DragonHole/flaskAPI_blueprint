#!/bin/sh
export FLASK_APP=./project/index.py
pipenv run flask --app app --debug run --host=0.0.0.0 --port=3000