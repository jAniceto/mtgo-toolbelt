import os
import json
import time
import datetime
import requests
import json
from tqdm import tqdm


DECKS_FILE = '../deck-exporter/decks.json'


# Dictionary to convert deck family to a list of color codes
COLORS = dict(white=['w'], blue=['u'], black=['b'], red=['r'], green=['g'], selesnya=['w', 'g'],
              orzhov=['w', 'b'], boros=['w', 'r'], azorius=['w', 'u'], dimir=['u', 'b'],
              rakdos=['b', 'r'], golgari=['b', 'g'], izzet=['u', 'r'], simic=['u', 'g'],
              gruul=['r', 'g'], naya=['w', 'r', 'g'], esper=['w', 'u', 'b'], grixis=['u', 'b', 'r'],
              jund=['b', 'r', 'g'], bant=['w', 'u', 'g'], abzan=['w', 'b', 'g'],
              temur=['u', 'r', 'g'], jeskai=['w', 'u', 'r'], mardu=['w', 'b', 'r'],
              sultai=['u', 'b', 'g'], glint=['u', 'b', 'r', 'g'], dune=['w', 'b', 'r', 'g'],
              ink=['w', 'u', 'r', 'g'], whitch=['w', 'u', 'b', 'g'], yore=['w', 'u', 'b', 'r'],
              domain=['w', 'u', 'b', 'r', 'g'], colorless=['c'])


# Dictionary to store card info
CARD_INFO_DICT = {}


def load_decks():
    with open(DECKS_FILE, 'r') as f:
        decks = json.load(f)
    return decks


def clean_file_path(fp):
    working_dir = os.path.dirname(__file__)
    cleaned_fp = os.path.join(working_dir, fp)
    return cleaned_fp


def get_path(name):
    """
    Returns the deck path from name
    """
    path = f'../deck-exporter/decks/ready/{name}.txt'
    return path


def sort_card_list(card_list):
    """
    Sorts a list of card objects (dictionaries) by converted mana cost (placing lands first)
    :param card_list: card_list is a list of dictionaries containing info on quantity, card_name, mc, cmc, and is_land
    :return: sorted_list, a card list sorted according to the defined order
    """

    sorted_list = card_list
    sorted_list.sort(key=lambda k: k['is_land'], reverse=True)
    sorted_list.sort(key=lambda k: k['cmc'])

    return sorted_list


def store_card_info(card_info):
    global CARD_INFO_DICT
    CARD_INFO_DICT[card_info['name']] = card_info


def scryfall(card_name, store=False):
    # Get list of all cards with a name: https://api.scryfall.com/cards/search?order=released&q=%2B%2B%21%22Rancor%22
    query = '++!"{}"'.format(card_name)
    params = {
        'order': 'tix',
        'unique': 'prints',
        'q': query
        }
    r = requests.get('https://api.scryfall.com/cards/search', params=params)
    reprint_dict = r.json()

    # Create return dict
    card_info = {'name': card_name,
                 'prices': [],
                 'best_price': None}

    # Get prices of all reprints
    for reprint in reprint_dict['data']:
        # Only do stuff for reprints available on MTGO
        if reprint['prices']['tix']:
            card_info['prices'].append([reprint['set'].upper(), reprint['prices']['tix']])

    if card_info['prices']:
        # card_info['best_price'] = str(min([float(set_price[1]) for set_price in card_info['prices']]))
        card_info['best_price'] = min(card_info['prices'], key=lambda x:float(x[1]))
    else:
        print(f'WARNING: No price found for {card_info["name"]}')

    # Get card data
    card_info['scryfall_uri'] = reprint_dict['data'][-1]['scryfall_uri']
    card_info['cmc'] = reprint_dict['data'][-1]['cmc']
    card_info['legalities'] = reprint_dict['data'][-1]['legalities']
    try:
        card_info['image_uris'] = reprint_dict['data'][-1]['image_uris']
        card_info['mana_cost'] = reprint_dict['data'][-1]['mana_cost']
        card_info['colors'] = reprint_dict['data'][-1]['colors']
        card_info['type'] = reprint_dict['data'][-1]['type_line']
    except KeyError:  # handles card with multiple faces
        card_info['image_uris'] = reprint_dict['data'][-1]['card_faces'][0]['image_uris']
        card_info['image_uris_2'] = reprint_dict['data'][-1]['card_faces'][1]['image_uris']
        card_info['mana_cost'] = reprint_dict['data'][-1]['card_faces'][0]['mana_cost']
        card_info['colors'] = reprint_dict['data'][-1]['card_faces'][0]['colors']
        card_info['type'] = reprint_dict['data'][-1]['card_faces'][0]['type_line']

    if 'Land' in card_info['type']:
        card_info['is_land'] = True
    else:
        card_info['is_land'] = False

    if store:
        store_card_info(card_info)

    return card_info


def parse_decklist(deck_file):
    """
    Parses a decklist file
    """
    is_mainboard=True
    mainboard=[]
    sideboard=[]
    with open(deck_file, 'r') as f:
        for line in f:
            if line in ['\n', '\r\n']:
                is_mainboard=False
            else:
                card_line=line.strip('\n').split(' ', 1)
                if is_mainboard:
                    mainboard.append({'quantity': card_line[0],
                                      'card_name': card_line[1]})
                else:
                    sideboard.append({'quantity': card_line[0],
                                      'card_name': card_line[1]})

    # Get card info
    for card in mainboard:
        try:
            card.update(CARD_INFO_DICT[card['card_name']])
        except KeyError:
            card.update(scryfall(card['card_name'], store=True))
            time.sleep(50/1000)

    for card in sideboard:
        try:
            card.update(CARD_INFO_DICT[card['card_name']])
        except KeyError:
            card.update(scryfall(card['card_name'], store=True))
            time.sleep(50/1000)

    # Sort decklist by converted mana cost
    sorted_mainboard=sort_card_list(mainboard)
    sorted_sideboard=sort_card_list(sideboard)
    mainboard=sorted_mainboard
    sideboard=sorted_sideboard

    return mainboard, sideboard


def main():
    start_time=time.time()
    print('Grabbing data...')

    # Get list of decks for input file (decks.py)
    deck_list=load_decks()
    total_decks=len(deck_list)

    # Sort list of decks by deck name
    all_decks=sorted(deck_list, key=lambda k: k['name'])

    progress_bar = tqdm(all_decks)
    for i, deck in enumerate(progress_bar):
        # Get list of colors from family
        if deck['family']:
            deck['color'] = COLORS[deck['family']]

        try:
            # Get path to deck file
            deck['path'] = get_path(deck['name'])

            # Get last modified date
            date_modified_datetime=datetime.datetime.fromtimestamp(
                os.path.getmtime(deck['path']))
            date_modified_string=date_modified_datetime.strftime('%Y-%m-%d')
            deck['last_modified']=date_modified_string

        except FileNotFoundError as e:
            print(f"\nDeck file not found for {deck['name']}! ({e})")
            continue

        # Parse decklist from file
        deck['mainboard'], deck['sideboard'] = parse_decklist(deck['path'])

        # Calculated decklist price
        price = 0
        for card in deck['mainboard']:
            if card['best_price']:
                price += float(card['best_price'][1])
        for card in deck['sideboard']:
            if card['best_price']:
                price += float(card['best_price'][1])
        deck['price'] = '{:.2f}'.format(price)

        # print(f"\nDeck {i + 1} of {total_decks} completed! ({deck['name']})")
        progress_bar.set_description(f"Completed {deck['name']}")

    # Save deck data to JSON
    with open(clean_file_path('decks.json'), 'w') as decks_json:
        json.dump(all_decks, decks_json, sort_keys=True, indent=2)

    # Save card data to JSON
    with open(clean_file_path('cards.json'), 'w') as cards_json:
        json.dump(CARD_INFO_DICT, cards_json, sort_keys=True, indent=2)

    print('\nCompleted in {0:.1f} minutes'.format((time.time() - start_time)/60))


if __name__ == '__main__':
    main()
