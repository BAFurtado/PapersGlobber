import json
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt


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
    print('-' * 100, len(all_journals), ': JOURNALS', '-' * 100)
    for tag, count in sorted(tag_journals.items(), key=lambda x: x[1], reverse=True):
        print(f'{tag}: {count}')

    all_abstracts = [item['abstractNote'] for item in data if 'abstractNote' in item]
    abstract_words = [' '.join(a.split()) for a in all_abstracts]
    return data, abstract_words


def getting_authors(data):
    # Initialize an empty list to store last names
    last_names = list()
    for paper in data:
        # Check the dictionary
        if 'creators' in paper:
            for author in paper['creators']:
                if 'lastName' in author:
                    last_names.append(author['lastName'])
    last_names_counter = Counter(last_names)
    print('-' * 100, len(last_names_counter), ': AUTHORS', '-' * 100)
    for tag, count in sorted(last_names_counter.items(), key=lambda x: x[1], reverse=True):
        print(f'{tag}: {count}')
    return last_names


if __name__ == '__main__':
    f = 'results.json'
    d, abs_words = main(f)
    combined_text = ' '.join(abs_words)

    # Create a WordCloud object
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(combined_text)

    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('image.png')
    plt.show()

    last = getting_authors(d)
