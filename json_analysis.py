import json
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def getting_keywords(data):
    # Keywords when available
    all_tags = [tag_dict['tag']
                .lower()
                .replace('-', ' ')
                .replace('modell', 'model')
                .replace('modeling', 'model')
                .replace(' (abm) ', '')
                for item in data
                for tag_dict in item.get('tags', [])]
    tag_counts = Counter(all_tags)
    print('-' * 100, 'KEYWORDS', '-' * 100)
    print(f'There are {len(all_tags)} keywords, considering the {len(data)} found papers')
    for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True):
        print(f'{tag.capitalize()}: {count}')
    return all_tags


def getting_journals(data):
    all_journals = [item['publicationTitle'].lower() for item in data if 'publicationTitle' in item]
    tag_journals = Counter(all_journals)
    print('-' * 100, len(all_journals), ': JOURNALS', '-' * 100)
    for tag, count in sorted(tag_journals.items(), key=lambda x: x[1], reverse=True):
        print(f'{tag.upper()}: {count}')
    return all_journals


def getting_abstracts(data):
    all_abstracts = [item['abstractNote'] for item in data if 'abstractNote' in item]
    return all_abstracts


def getting_authors(data):
    # Initialize an empty list to store last names
    names = list()
    for paper in data:
        # Check the dictionary
        if 'creators' in paper:
            for author in paper['creators']:
                if 'lastName' in author:
                    if 'firstName' in author:
                        # Getting just the first initial
                        initials = author['firstName'].split(' ')[0][0]
                        names.append(f"{author['lastName']}, {initials}")
                    else:
                        names.append(author['lastName'])
    names_counter = Counter(names)
    print('-' * 100, len(names_counter), ': AUTHORS', '-' * 100)
    for tag, count in sorted(names_counter.items(), key=lambda x: x[1], reverse=True):
        print(f'{tag}: {count}')
    return names


def getting_titles():
    pass


def word_cloud(list_words):
    abstract_words = [' '.join(a.split()) for a in list_words]
    combined_text = ' '.join(abstract_words)

    # Create a WordCloud object
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(combined_text)

    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('image.png')
    plt.show()


def main(file_address):
    # Load the JSON data
    with open(file_address, 'r') as json_file:
        data = json.load(json_file)
    keys = getting_keywords(data)
    journals = getting_journals(data)
    abstracts = getting_abstracts(data)
    authors = getting_authors(data)
    return keys, journals, abstracts, authors


if __name__ == '__main__':
    f = 'results.json'
    k, j, abst, aut = main(f)
