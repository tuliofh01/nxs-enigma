#!python3

import curses
import src.misc.config as global_config_variables

from src.tui.windows.empty_window import EmptyWindow

class ErrorState:

    def __init__(self):
        self.art = str()
        art_path = global_config_variables.ERROR_ART_PATH
        with open(art_path, "r") as error_characters:
            for character_line in error_characters.readlines():
                self.art += character_line

    def toggle_state(self, target_window: EmptyWindow) -> None:
        lines = target_window.main_window.getyx()[1]
        columns = target_window.main_window.getyx()[0]

        target_window.main_window.addstr(
            ( (lines/2) - (9/2) ),
            (  (columns/2) - int(44/2) ),
            self.art, curses.color_pair(1)
        )

        target_window.main_window.getkey()
        target_window.main_window.erase()
        target_window.refresh()
