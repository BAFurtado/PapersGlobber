import json


def main(file_address):
    with open(f'{file_address}.json', 'r') as file:
        results = json.load(file)

    print(f'Currently, {len(results)} papers in database')
    keys = [results[i]['key'] for i in range(len(results))]
    # Verify no repeated keys
    if len(set(keys)) != len(results):
        print('There are repeated keys!')
        results = list(
            {
                dictionary['id']: dictionary
                for dictionary in results
            }.values()
        )
        print(f'After dropping duplicates, there are {len(results)} papers in database')
        with open(f'{file_address}_no_duplicates.json', 'w') as file:
            json.dump(results, file)
    return results


if __name__ == '__main__':
    f = 'results'
    d = main(f)
