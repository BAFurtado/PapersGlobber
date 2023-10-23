import json
import os
import time

import pandas as pd

time.sleep(20)


def run_list_translators():
    f = 'tweets.csv'
    g = 'new_tweets.csv'
    data, new = check_data_before_loading(f, g)
    data = data.address.to_list()
    file_address = 'results.json'
    try:
        with open(file_address, 'r') as file:
            results = json.load(file)
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
                    print('x' * 100, '\n', response_doi, ': ', url_search)
            if output:
                results += output
                print(output)
        if i % 10 == 0:
            with open(file_address, 'w') as json_file:
                json.dump(results, json_file, indent=4)
    print('Overwriting new tweets into tweets.csv')
    new.to_csv('tweets.csv', index=False)


def check_data_before_loading(old, new):
    old = pd.read_csv(old, names=['id', 'address'])
    new = pd.read_csv(new, names=['id', 'address'])
    unique_df = new[~new['address'].isin(old['address'])]
    print(f'Checking {len(unique_df)} new papers...')
    return unique_df, new


if __name__ == '__main__':
    run_list_translators()
