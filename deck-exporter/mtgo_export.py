"""
Script to automate exporting MTGO decks to file. 
Automates the mouse and keyboard movement required to export 

Notes:
- You must have MTGO client open.
- You must be on the Collection page.
- You must select the first deck to export.
- Only decks in the selected deck category are exported.
- The DECK variable in the configuration section below defines how many decks are exported.
- You can not change windows while the script is running.
"""

import pyautogui
import time
import sys


# Configuration
DECKS = 312  # Number of decks (how many saves are attempted)


pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True


def focus_mtgo_window():
    "Focus the MTGO window by clicking the title bar (top)"
    pyautogui.click(338, 9, button='left')


def main():
    # Check if first deck is selected
    prep = input('Have you selected the first deck you want to export? ([y]/n): ')
    if prep not in ['', 'y', 'yes', 'Y', 'Yes']:
        sys.exit('Please select the first deck you want to export and run the script again.')

    print("works")

    # Focus MTGO window
    focus_mtgo_window()

    # Scroll over decks and export
    deck_count = 1
    while True:
        # Log current deck to console
        print(f'Exporting Deck {deck_count}...')

        # Press context menu key
        pyautogui.hotkey('shift','f10')
        # pyautogui.hotkey('apps')

        # Use keyboard to select Export from the context menu
        pyautogui.typewrite(['down', 'down', 'down', 'down', 'enter'])

        # Use keyboard to select file type and save
        pyautogui.typewrite(['tab', 'down', 'down', 'enter', 'enter'])

        # Focus MTGO window
        focus_mtgo_window()
        
        # Press down to go to next deck
        pyautogui.press('down')

        deck_count += 1

        if deck_count == DECKS:
            break


if __name__ == '__main__':
    main()