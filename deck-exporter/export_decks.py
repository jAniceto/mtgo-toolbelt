import pyautogui
from config import *


pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True


def export_menu(x, y):
    """
    Makes the necessary clicks to export deck

    args:
        x : int, x-axis position in pixels
        y : int, y-axis position in pixels

    returns:
        x : int, x-axis position in pixels (updated)
        y : int, y-axis position in pixels (updated)
    """
    # Move to deck right click
    pyautogui.click(x, y, button='right')

    # Left click Export
    pyautogui.click(x + 10, y + STEP*4.5, button='left')

    # Use keyboard to select file type and save: TAB, DOWN, DOWN, ENTER
    pyautogui.typewrite(['tab', 'down', 'down', 'enter', 'enter'])

    return x, y


def main():
    while True:
        # Reset position to top of list
        x = START_X
        y = START_Y
        
        # Export all current visible decks in the list
        deck_count = 0
        for i in range(0, DECKS_PER_SCREEN):
            deck_count += 1

            # Log current deck to console
            print(f'Exporting Deck {deck_count}...')

            # Save deck
            x, y = export_menu(x, y)
            
            y += STEP

        # Scroll down the list by clicking the down arrow SCROLL_CLICKS times 
        # (requests confirmation if FULL_AUTO is False)
        if not FULL_AUTO:
            txt = input("Continue ([y]/n): ")
            if txt == 'n':
                break

        for i in range(0, SCROLL_CLICKS):
            pyautogui.click(223, 926, button='left')


if __name__ == '__main__':
    main()