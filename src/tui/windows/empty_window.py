#!python3

import curses
from src.misc.config import CONFIG


class EmptyWindow:

    def __init__(self):
        curses.curs_set(0)
        curses.resizeterm(CONFIG["tui"]["default_height"], CONFIG["tui"]["default_width"])

        curses.start_color()
        curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(11, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(12, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(13, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.custom_colors = range(10, 13)

        self.main_window = curses.initscr()

    def refresh(self):
        self.main_window.refresh()
        curses.doupdate()

    def clear(self):
        self.main_window.clear()
        curses.doupdate()

    @staticmethod
    def flash():
        curses.flash()

    @staticmethod
    def close():
        curses.endwin()

    @staticmethod
    def sleep(seconds):
        curses.napms(seconds * 1000)

