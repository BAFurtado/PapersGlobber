import json
from collections import Counter


def main(file_address):
    # Load the JSON data
    with open(file_address, 'r') as json_file:
        data = json.load(json_file)

    # Keywords when available
    all_tags = [tag_dict['tag'] for item in data for tag_dict in item.get('tags', [])]
    tag_counts = Counter(all_tags)
    print('-' * 100, 'KEYWORDS', '-' * 100)
    print(f'There are {len(all_tags)} keywords, considering the {len(data)} found papers')
    for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True):
        print(f'{tag}: {count}')

    all_journals = [item['publicationTitle'] for item in data if 'publicationTitle' in item]
    tag_journals = Counter(all_journals)
    print('-' * 100, 'JOURNALS', '-' * 100)
    for tag, count in sorted(tag_journals.items(), key=lambda x: x[1], reverse=True):
        print(f'{tag}: {count}')

    all_abstracts = [item['abstractNote'] for item in data if 'abstractNote' in item]
    return data


if __name__ == '__main__':
    f = 'results.json'
    d = main(f)
