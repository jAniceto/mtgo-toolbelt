# mtgo-toolbelt
A collection of tools for Magic Online


## Deck Exporter

Export MTGO decks to .txt files automatically using `pyautogui`.

```
$ cd deck-exporter
$ python mtgo_export.py  # export MTGO decks
$ python organize.py  # organize exported decks
$ python update_info.py  # update decks.json with exported decks
$ python utils.py  # run utility functions
```

Edit the created `decks_new.json` file to provide additional info. 
Delete the old `decks.json` file and rename `decks_new.json` to `decks.json`.
Scripts in the `scryfall` folder use the `decks.json` file as input.


### `mtgo_export.py` script

Script to automate exporting MTGO decks to file. 
Automates the mouse and keyboard movement required to export 

Notes:
- You must have MTGO client open.
- You must be on the Collection page.
- You must select the first deck to export.
- Only decks in the selected deck category are exported.
- The DECK variable in the configuration section below defines how many decks are exported.
- You can not change windows while the script is running.


## Scryfall

Under construction