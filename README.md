
# Demo of how to make big_query work.

Not really meant for public consumption

## Notes:
to activate local env:
 source bigtable/bin/activate     

BigTable key:

    Go through the dance to get your key here:
    https://cloud.google.com/docs/authentication/getting-started#cloud-console

    Save the key locally (In my case: key.json) and add it as an env variable:
    export GOOGLE_APPLICATION_CREDENTIALS="key.json"
    
See output in big query [here](https://console.cloud.google.com/bigquery?project=learning-bigtable-2021&ws=!1m24!1m3!3m2!1slearning-bigtable-2021!2stesting!1m4!4m3!1slearning-bigtable-2021!2stesting!3sfrom-nc2!1m4!4m3!1slearning-bigtable-2021!2stesting!3snc2!1m4!4m3!1slearning-bigtable-2021!2stesting!3swindow_function_data!1m4!4m3!1slearning-bigtable-2021!2stesting!3swindow_functions!1m0&j=bq:EU:bquxjob_9aba5d9_17a4233926e&page=queryresults)
