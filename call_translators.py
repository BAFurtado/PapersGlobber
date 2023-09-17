import json
import os
import time

import pandas as pd

time.sleep(20)


def run_list_translators(data):
    file_address = 'results.json'
    try:
        with open(file_address, 'r') as file:
            results = json.load(file)
            data = data[len(results):]
    except FileNotFoundError:
        results = list()

    url = 'http://127.0.0.1:1969/web'
    url_search = 'http://127.0.0.1:1969/search'
    headers = 'Content-Type: text/plain'

    for i, page in enumerate(data):
        print('-' * 100)
        # Using curl to make a POST request
        cmd = f"curl -d '{page}' -H '{headers}' '{url}' --silent"
        response = os.popen(cmd).read()
        if response:
            try:
                output = json.loads(response)
            except json.JSONDecodeError:
                print('x' * 100, '\n', response)
                continue
            if 'DOI' in output[0]:
                # Using curl to make a POST request for DOI
                cmd_doi = f"curl -d '{output[0]['DOI']}' -H '{headers}' '{url_search}' --silent"
                response_doi = os.popen(cmd_doi).read()
                try:
                    output = json.loads(response_doi)
                except json.JSONDecodeError:
                    print('x' * 100, '\n', response_doi)
            if output:
                results += output
                print(output)
        if i % 10 == 0:
            with open('results.json', 'w') as json_file:
                json.dump(results, json_file, indent=4)


if __name__ == '__main__':
    f = 'tweets.csv'
    d = pd.read_csv('tweets.csv', names=['id', 'address'])
    d = d.address.to_list()
    run_list_translators(d)
