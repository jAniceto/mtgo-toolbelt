import requests
import pprint


def scryfall(card_name):
    """
    Get relevant card info from Scyfall API.

    Parameters
    ----------
    card_name : str
        Name of card to search.

    Returns
    -------
    card_info : dict
        Dictionary of relevant card properties.

    Example output
    --------------
    {
        'name': 'Rancor',
        'prices': [
            ['PC2', '1.56'],
            ['DDD', '1.25'], ...
        ],
        'best_price': ['A25', '0.93'],
        'scryfall_uri': 'https://scryfall.com/card/f05/1/rancor?utm_source=api',
        'cmc': 1.0,
        'legalities': {
            'pioneer': 'not_legal',
            'modern': 'legal',
            'pauper': 'legal', ...
        },
        'image_uris': {
            'small': 'https://img.scryfall.com/cards/small/front/7/2/72a6c655-92f8-486d-b56c-9f6753f58512.jpg?1562639861',
            'normal': 'https://img.scryfall.com/cards/normal/front/7/2/72a6c655-92f8-486d-b56c-9f6753f58512.jpg?1562639861', ...
        },
        'mana_cost': '{G}',
        'colors': ['G'],
        'type': 'Enchantment — Aura',
        'is_land': False
    }
    """

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
        print(f'\nWARNING: No price found for {card_info["name"]}')

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

    return card_info


if __name__ == '__main__':
    pprint.pprint(scryfall('Rancor'))
