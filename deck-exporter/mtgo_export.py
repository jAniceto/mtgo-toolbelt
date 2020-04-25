import pyautogui
import time


# Configuration
DECKS = 320  # Number of decks (how many saves are attempted)
START_X = 16  # X start position in pixels for first deck (depends on screen resolution)
START_Y = 372  # Y start position in pixels for first deck (depends on screen resolution)


pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True


def main():
    # Reset position to top of list
    x = START_X
    y = START_Y
    pyautogui.click(START_X, START_Y, button='left')

    deck_count = 1
    # Scroll over decks and export
    while True:
        # Log current deck to console
        print(f'Exporting Deck {deck_count}...')

        # Press context menu key
        pyautogui.hotkey('shift','f10')

        # Click Export
        pyautogui.click(59, 620, button='left')

        # Use keyboard to select file type and save: TAB, DOWN, DOWN, ENTER
        pyautogui.typewrite(['tab', 'down', 'down', 'enter', 'enter'])

        # Focus MTGO window
        pyautogui.click(338, 9, button='left')
        
        # Press down to go to next deck
        pyautogui.press('down')

        deck_count += 1

        if deck_count == DECKS:
            break


if __name__ == '__main__':
    main()