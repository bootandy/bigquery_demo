#!/bin/sh

export GOOGLE_APPLICATION_CREDENTIALS="key.json"

cd /home/andy/bigquery_demo/
/home/andy/.virtualenvs/bigquery_demo/bin/python   src/__init__.py  /var/log/window_functions.log

