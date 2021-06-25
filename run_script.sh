#!/bin/sh

export GOOGLE_APPLICATION_CREDENTIALS="key.json"

cd /home/andy/bigquery_demo/
file=`ls -t /var/log/old_win_func/window_functions* | head  -1`

/home/andy/.virtualenvs/bigquery_demo/bin/python   src/__init__.py  $file

