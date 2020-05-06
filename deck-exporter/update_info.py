import json
import os


# Configuration
DECKS_DIR = 'decks'
OLD_FILENAME = 'decks.json'
NEW_FILENAME = 'decks_new.json'


def search_deck(name, deck_list):
    """
    Given a deck name, return the deck info dictionary in it exist in a given list of deck dictionaries.
    """
    for d in deck_list:
        if d['name'] == name:
            return d
    return None


def find_family(deck_name):
    """
    Given a deck name, try to find the deck family.
    """
    FAMILIES = ['white', 'blue', 'black', 'red', 'green', 'selesnya', 'orzhov', 'boros', 'azorius', 'dimir', 'rakdos', 'golgari', 'izzet', 'simic', 'gruul', 'naya', 'esper', 'grixis', 'jund', 'bant', 'abzan', 'temur', 'jeskai', 'mardu', 'sultai', 'glint', 'dune', 'ink', 'whitch', 'yore', 'domain', 'colorless']
    for family in FAMILIES:
        if family in deck_name.lower():
            return family


def main():
    """
    Create new deck info dictionary.
    """
    # Get old deck data
    with open(OLD_FILENAME, 'r') as f:
        decks_old = json.load(f)

    # Get new decks
    deck_files = [f for f in os.listdir(os.path.join(DECKS_DIR, 'ready')) if os.path.isfile(os.path.join(DECKS_DIR, 'ready', f))]

    # Create new deck data
    deck_info = []
    for deck_name in deck_files:
        deck_name = deck_name.replace('.txt', '')
        # Create deck entry
        info = {
            'name': deck_name,
            'tags': [],
            'family': None,
            'source': {'name': None, 'link': None}
        }

        # Check for deck info in previous json deck info file 
        prev_deck_info = search_deck(deck_name, decks_old)

        if prev_deck_info:
            # Update new deck dictionary with previous info
            info['tags'] = prev_deck_info['tags']
            info['family'] = prev_deck_info['family']
            info['source'] = prev_deck_info['source']
        else:
            # TO DO: Fill deck family info from deck name (if possible)
            info['family'] = find_family(deck_name)

        deck_info.append(info)

    with open(NEW_FILENAME, 'w') as f:
        json.dump(deck_info, f, indent=4)


if __name__ == '__main__':
    main()