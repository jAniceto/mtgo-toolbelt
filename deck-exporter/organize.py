import os


# Configuration
BASE_DIR = 'decks'
SUB_DIRS = ['banned', 'ready']
BANNED_CARDS = ['Daze', 'Gitaxian Probe', 'Gush', "Arcum's Astrolabe"]
STRIP_CHARS = ['#T1 ', '#T2 ', '.txt']
ORGANIZE = True


def create_sub_dirs(base_dir, subdirs):
    """
    Create required folders.
    """
    for subdir in subdirs:
        if not os.path.exists(os.path.join(base_dir, subdir)):
            os.mkdir(os.path.join(base_dir, subdir))


def clean_file_names(filename, chars_to_strip):
    """
    Clean deck filenames.
    """
    tmp = filename
    for char in chars_to_strip:
        tmp = tmp.strip().strip('!').replace(char, '').strip()
    new_filename = tmp + '.txt'

    if filename != new_filename:
        os.rename(os.path.join(BASE_DIR, filename), os.path.join(BASE_DIR, new_filename))


def organize_decks(filename, ban_list):
    """
    Move deck to respective folder.
    """
    with open(os.path.join(BASE_DIR, filename), 'r') as f:
        data = f.read()
    
    if any(card in data for card in ban_list):
        os.rename(os.path.join(BASE_DIR, filename), os.path.join(BASE_DIR, 'banned', filename))
    else:
        os.rename(os.path.join(BASE_DIR, filename), os.path.join(BASE_DIR, 'ready', filename))


def main():
    """
    Organize deck files into folders.
    """
    deck_files = [f for f in os.listdir(BASE_DIR) if os.path.isfile(os.path.join(BASE_DIR, f))]

    for deck_file in deck_files:
        clean_file_names(deck_file, STRIP_CHARS)

    if ORGANIZE == True:
        deck_files = [f for f in os.listdir(BASE_DIR) if os.path.isfile(os.path.join(BASE_DIR, f))]
        
        create_sub_dirs(BASE_DIR, SUB_DIRS)

        for deck_file in deck_files:
            organize_decks(deck_file, BANNED_CARDS)


if __name__ == '__main__':
    main()
