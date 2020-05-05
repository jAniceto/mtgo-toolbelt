import json
import os


BASE_DIR = ''


def dict_to_lists(dictionary):
    x = []
    y = []
    for key, value in dictionary.items():
        x.append(key)
        y.append(value)
    return x, y


def stats():
    # Load JSON deck data (from decks.json and cards.json)
    with open(os.path.join(BASE_DIR, 'decks.json'), 'r') as fp:
        decks = json.load(fp)

    with open(os.path.join(BASE_DIR, 'cards.json'), 'r') as fp:
        cards = json.load(fp)

    deck_count = len(decks)

    # Get card counts and frequency
    card_deck = {}
    for deck in decks:
        mainboard_cards = []  # keeps track of mainboard cards
        for card in deck['mainboard']:
            mainboard_cards.append(card['card_name'])
            try:
                card_deck[card['card_name']]['count'] += 1
                card_deck[card['card_name']]['total_count'] += int(card['quantity'])
            except KeyError:
                card_deck.update({card['card_name']: {'count': 1,
                                                      'total_count': int(card['quantity'])}})

        for card in deck['sideboard']:
            try:
                if card['card_name'] not in mainboard_cards:  # if card is already in mainboard don't count it
                    card_deck[card['card_name']]['count'] += 1
                card_deck[card['card_name']]['total_count'] += int(card['quantity'])
            except KeyError:
                card_deck.update({card['card_name']: {'count': 1,
                                                      'total_count': int(card['quantity'])}})

    for key, value in card_deck.items():
        card_deck[key]['frequency'] = value['count']/deck_count*100
        card_deck[key]['avg'] = value['total_count'] / value['count']

    # Get deck color distribution
    deck_color_distribution = {'w': 0, 'u': 0, 'b': 0, 'r': 0, 'g': 0}
    for deck in decks:
        for key, value in deck_color_distribution.items():
            if key in deck['color']:
                deck_color_distribution[key] += 1

    deck_colors = {}
    deck_colors['colors'], deck_colors['frequency'] = dict_to_lists(deck_color_distribution)

    # Get deck family distribution
    deck_family_distribution = {'white': 0, 'blue': 0, 'black': 0, 'red': 0, 'green': 0,
                                'selesnya': 0, 'orzhov': 0, 'boros': 0, 'azorius': 0, 'dimir': 0,
                                'rakdos': 0, 'golgari': 0, 'izzet': 0, 'simic': 0, 'gruul': 0,
                                'naya': 0, 'esper': 0, 'grixis': 0, 'jund': 0, 'bant': 0,
                                'abzan': 0, 'sultai': 0, 'temur': 0, 'jeskai': 0, 'mardu': 0,
                                'domain': 0, 'colorless': 0}
    for deck in decks:
        for key, value in deck_family_distribution.items():
            if key == deck['family']:
                deck_family_distribution[key] += 1
                continue

    deck_family = {}
    deck_family['families'], deck_family['frequency'] = dict_to_lists(deck_family_distribution)

    # Create stats dictionary
    stats = {
        'cards': card_deck,
        'deck_colors': deck_color_distribution,
        'deck_families': deck_family_distribution
    }

    with open(os.path.join(BASE_DIR, 'stats.json'), 'w') as fp:
        json.dump(stats, fp, indent=4)


if __name__ == '__main__':
    stats()