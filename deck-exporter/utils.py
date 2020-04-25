import json


def get_tag_list(file_path):
    """
    Print a list of unique tags
    """
    with open(file_path, 'r') as deck_json:
        deck_list = json.load(deck_json)

    tag_list = []
    for deck in deck_list:
        for tag in deck['tags']:
            if tag not in tag_list:
                tag_list.append(tag)

    sorted_tag_list = sorted(tag_list, key=str.lower)
    print('Alphabetically sorted tag list:')
    print(sorted_tag_list)


if __name__ == '__main__':
    get_tag_list('decks/decks.json')