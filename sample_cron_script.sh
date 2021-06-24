# Type:
# crontab -e
# and add this:

0 5 * * * /home/andy/bigquery_demo/run_script.sh >>/var/log/bigquery_demo.log 2>&1

