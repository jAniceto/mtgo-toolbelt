import os
import json
import time
import datetime
import logging
from tqdm import tqdm
import scryfall


# Current deck file
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


# Logging config
logging.basicConfig(filename='log.txt', filemode='w', level=logging.INFO)


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


def parse_decklist(deck_file):
    """
    Parses a decklist file
    """
    is_mainboard = True
    mainboard = []
    sideboard = []
    with open(deck_file, 'r') as f:
        for line in f:
            if line in ['\n', '\r\n']:
                is_mainboard = False
            else:
                card_line = line.strip('\n').split(' ', 1)
                if is_mainboard:
                    mainboard.append({'quantity': card_line[0],
                                      'card_name': card_line[1]})
                else:
                    sideboard.append({'quantity': card_line[0],
                                      'card_name': card_line[1]})

    # Get card info
    for card in mainboard:
        try:
            # Try to grab info from cache dict
            card.update(CARD_INFO_DICT[card['card_name']])
        except KeyError:
            # If info not in cache grab it from Scryfall API and update cache
            card_info = scryfall.scryfall(card['card_name'])
            card.update(card_info)
            store_card_info(card_info)
            time.sleep(50/1000)

    for card in sideboard:
        try:
            # Try to grab info from cache dict
            card.update(CARD_INFO_DICT[card['card_name']])
        except KeyError:
            # If info not in cache grab it from Scryfall API and update cache
            card_info = scryfall.scryfall(card['card_name'])
            card.update(card_info)
            store_card_info(card_info)
            time.sleep(50/1000)

    # Sort decklist by converted mana cost
    sorted_mainboard = sort_card_list(mainboard)
    sorted_sideboard = sort_card_list(sideboard)
    mainboard = sorted_mainboard
    sideboard = sorted_sideboard

    return mainboard, sideboard


def main():
    start_time = time.time()
    print('Grabbing data...')
    logging.info('Grabbing data...')

    # Get current list of decks (decks.json)
    deck_list = load_decks()
    total_decks = len(deck_list)
    logging.info(f'Processing {total_decks} decks.')

    # Sort list of decks by deck name
    all_decks = sorted(deck_list, key=lambda k: k['name'])

    all_decks_list = []
    progress_bar = tqdm(all_decks)
    for i, deck in enumerate(progress_bar):
        # Get list of colors from family
        if deck['family']:
            deck['color'] = COLORS[deck['family']]
        else:
            logging.info(f"No specified family for deck {deck['name']}.")

        try:
            # Get path to deck file
            deck_path = get_path(deck['name'])
            # Get last modified date
            date_modified_datetime = datetime.datetime.fromtimestamp(os.path.getmtime(deck_path))
            date_modified_string = date_modified_datetime.strftime('%Y-%m-%d')
            deck['last_modified'] = date_modified_string

        except FileNotFoundError as e:
            print(f"\nDeck file not found for {deck['name']}! ({e})")
            logging.warning(f"Deck file not found for {deck['name']}! ({e}).") 
            continue

        # Parse decklist from file
        deck['mainboard'], deck['sideboard'] = parse_decklist(deck_path)

        # Calculated decklist price
        price = 0
        for card in deck['mainboard']:
            if card['best_price']:
                price += float(card['best_price'][1])
        for card in deck['sideboard']:
            if card['best_price']:
                price += float(card['best_price'][1])
        deck['price'] = '{:.2f}'.format(price)

        all_decks_list.append(deck)

        # print(f"\nDeck {i + 1} of {total_decks} completed! ({deck['name']})")
        progress_bar.set_description(f"Completed {deck['name']}")
    
    # Save deck data to JSON
    with open(clean_file_path('decks.json'), 'w') as decks_json:
        json.dump(all_decks_list, decks_json, sort_keys=True, indent=2)

    # Save card data to JSON
    with open(clean_file_path('cards.json'), 'w') as cards_json:
        json.dump(CARD_INFO_DICT, cards_json, sort_keys=True, indent=2)

    # Save deck data to JSON (simple)
    KEYS_TO_REMOVE = ['card_name', 'prices', 'best_price', 'scryfall_uri', 'cmc', 'legalities', 'image_uris', 'mana_cost', 'colors', 'type', 'is_land']
    for deck in all_decks_list:
        for card in deck['mainboard']:
            for k in KEYS_TO_REMOVE:
                card.pop(k, None)
    with open(clean_file_path('decks_simple.json'), 'w') as decks_simple_json:
        json.dump(all_decks_list, decks_simple_json, sort_keys=True, indent=2)

    print('\nCompleted in {0:.1f} minutes'.format((time.time() - start_time)/60))
    logging.info('Completed in {0:.1f} minutes'.format((time.time() - start_time)/60))
    

if __name__ == '__main__':
    main()
