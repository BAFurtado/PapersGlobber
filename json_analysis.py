import json
from collections import Counter

import matplotlib.pyplot as plt
from wordcloud import WordCloud


def tokenize(list_words):
    return [w.lower()
            .strip()
            .replace(':', '')
            .replace('-', ' ')
            .replace(',', '')
            .replace('models', 'model')
            .replace('modell', 'model')
            .replace('modeling', 'model')
            .replace('(abm)', '')
            for w in list_words]


def getting_keywords(data):
    # Keywords when available
    all_tags = [tag_dict['tag']
                for item in data
                for tag_dict in item.get('tags', [])]
    all_tags = tokenize(all_tags)
    tag_counts = Counter(all_tags)
    print('-' * 100, 'KEYWORDS', '-' * 100)
    print(f'There are {len(all_tags)} keywords, considering the {len(data)} found papers')
    i = 0
    for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True):
        print(f'{tag.capitalize()}: {count}')
        i += 1
        if i > 9:
            break
    return all_tags


def getting_journals(data):
    all_journals = [item['publicationTitle'].lower() for item in data if 'publicationTitle' in item]
    tag_journals = Counter(all_journals)
    print('-' * 100, len(all_journals), ': JOURNALS', '-' * 100)
    i = 0
    for tag, count in sorted(tag_journals.items(), key=lambda x: x[1], reverse=True):
        print(f'{tag.upper()}: {count}')
        i += 1
        if i > 9:
            break
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
    i = 0
    for tag, count in sorted(names_counter.items(), key=lambda x: x[1], reverse=True):
        print(f'{tag}: {count}')
        i += 1
        if i > 9:
            break
    return names


def getting_titles(data):
    all_titles = [item['title'] for item in data if 'title' in item]
    all_titles = tokenize(all_titles)
    return all_titles


def getting_dates():
    pass


def word_cloud(list_words, name='image'):
    abstract_words = [' '.join(a.split()) for a in list_words]
    combined_text = ' '.join(abstract_words)

    # Create a WordCloud object
    wordcloud = WordCloud(width=800,
                          height=400,
                          colormap='hot',
                          background_color='black').generate(combined_text)

    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(f'{name}.png')
    plt.show()


def words_in_(data, search_word):
    # Receives a list of data and returns items that contain a given word
    return [w for w in data if search_word.lower() in w.lower()]


def main(file_address):
    # Load the JSON data
    with open(file_address, 'r') as json_file:
        data = json.load(json_file)
    keys = getting_keywords(data)
    journals = getting_journals(data)
    abstracts = getting_abstracts(data)
    authors = getting_authors(data)
    titles = getting_titles(data)
    return keys, journals, abstracts, authors, titles


if __name__ == '__main__':
    f = 'results_no_duplicates.json'
    k, j, abst, aut, t = main(f)
    word_cloud(k)
    word_cloud(t, 'title_image')
    policy_papers = words_in_(t, 'polic')
    oil = words_in_(t, 'oil')
