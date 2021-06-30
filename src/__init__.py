#!/usr/bin/python

from datetime import datetime
import json
from os import linesep
import sys
import io
from google.cloud import bigquery
# To view:
#SELECT * FROM `learning-bigtable-2021.testing.window_functions` LIMIT 1000

STATE_FILE = '.state'

class NoRowsException(Exception):
    pass


def upload_it(data_as_file):
    # Construct a BigQuery client object.
    client = bigquery.Client()
    table_id = "learning-bigtable-2021.testing.window_functions"
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON, autodetect=True,
    )

    job = client.load_table_from_file(data_as_file, table_id, job_config=job_config)
    job.result()  # Waits for the job to complete.

    table = client.get_table(table_id)  # Make an API request.
    print(
        "There are now {} rows and {} columns to {}".format(
            table.num_rows, len(table.schema), table_id
        )
    )


def build_data_from_query_line(line, now):
    if line.find('query') == 0:
        left = line.find("\"") + 1
        right = line.rfind("\"")
        query = line[left:right].strip()
        return {
            'query': query,
            'time': now,
        }
    return None


def read_file(filename, lines_already_processed):
    now = str(datetime.utcnow())
    f = open(filename, "r")
    lines = f.readlines()

    # Ignore lines already processed
    if lines_already_processed is not None:
        lines = [line for i, line in enumerate(lines) if i >= lines_already_processed]

    data = [build_data_from_query_line(line, now) for line in lines]
    return len(lines), data
    

def data_to_upload_format(data):
    as_json = [json.dumps(d) for d in data if d]
    print("Preparing {} rows for upload".format(len(as_json)))
    if not as_json:
        raise NoRowsException()
    as_json_str = "\n".join(as_json)
    return io.StringIO(as_json_str)


def main():
    if len(sys.argv) < 2:
        print("Please run with file to process as argument")
        return
    filenames = sys.argv

    filename_lines_read_pairing = get_state()

    
    for f in filenames:
        new_state, data = read_file(
            f, filename_lines_read_pairing.get(f)
        )
        try:
            upload_it(data_to_upload_format(data))
            filename_lines_read_pairing[f] = new_state
        except NoRowsException:
            print('No new query rows to process today')

    update_state(filename_lines_read_pairing)


def update_state(file_to_lines_read):
    f = open(STATE_FILE, "w")
    for name, lines_read in file_to_lines_read.items():
        f.write(str(name)+"\n")
        f.write(str(lines_read)+"\n")


"""
 This is a disgusting.
 We assume each of the files passed in will have a saved state
 If they don't we'll process the entire file.
 If the service is started multiple times in a day we'll only process
 the last 2 log files.
 But hey! It's an experiment
"""
def get_state():
    results = {}
    try:
        with open(STATE_FILE, "r") as f:
            content = f.readlines()
            while content:
                filename = content.next()
                lines_read = int(content.next())
                results[filename] = lines_read
        print('Processing from line {}'.format(lines_read))
    except:
        print('Failed to read state file resetting to 0')
    return results


if __name__ == "__main__":
    main()
