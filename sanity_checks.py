import json


def main(file_address):
    with open(f'{file_address}.json', 'r') as file:
        results = json.load(file)

    print(f'Currently, {len(results)} papers in database')
    keys_titles = {results[i]['key']: results[i]['title'] for i in range(len(results))}
    # Verify no repeated keys for the same title
    titles = list(set(keys_titles.values()))
    if len(keys_titles) != len(titles):
        print('There are repeated keys!')
        temp = list()
        res = dict()
        for key, val in keys_titles.items():
            if val not in temp:
                temp.append(val)
                res[key] = val
        results = [results[i] for i in range(len(results)) if results[i]['key'] in res]
        print(f'After dropping duplicates, there are {len(results)} papers in database')
        with open(f'{file_address}_no_duplicates.json', 'w') as file:
            json.dump(results, file)
    return results


if __name__ == '__main__':
    f = 'results'
    d = main(f)
