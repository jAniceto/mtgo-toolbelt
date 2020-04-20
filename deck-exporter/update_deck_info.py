import json
import os


# Configuration
BASE_DIR = 'D:\Downloads\MTGO decks'
OLD_FILENAME = 'decks_old.json'
NEW_FILENAME = 'deck_info.json'


def search_deck(name, deck_list):
    for d in deck_list:
        if d['name'] == name:
            return d
    return None


# Get old deck data
with open(os.path.join(BASE_DIR, OLD_FILENAME), 'r') as f:
    decks_old = json.load(f)

# Get new decks
deck_files = [f for f in os.listdir(os.path.join(BASE_DIR, 'ready')) if os.path.isfile(os.path.join(BASE_DIR, 'ready', f))]

# Create new deck data
deck_info = []
for deck_name in deck_files:
    # Create deck entry
    info = {
        'name': deck_name.strip('.txt'),
        'tags': [],
        'family': None,
        'source': {'name': None, 'link': None}
    }

    # Check for deck info in previous json deck info file 
    prev_deck_info = search_deck(deck_name.strip('.txt'), decks_old)

    if prev_deck_info:
        # Update new deck dictionary with previous info
        info['tags'] = prev_deck_info['tags']
        info['family'] = prev_deck_info['family']
        info['source'] = prev_deck_info['source']
    else:
        # TO DO: Fill deck family info from deck name (if possible)
        pass

    deck_info.append(info)

with open(os.path.join(BASE_DIR, NEW_FILENAME), 'w') as f:
    json.dump(deck_info, f, indent=4)

