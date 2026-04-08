#! python3

import curses
import src.misc.config as global_config_variables

from src.tui.windows.empty_window import EmptyWindow

class MainState():

    def __init__(self, window: EmptyWindow):
        # Initializes color pairs
        curses.init_pair(1, curses.COLOR_WHITE, 234)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_GREEN, 234)
        curses.init_pair(4, curses.COLOR_RED, 234)

        main_window = window
        side_display = curses.newwin(curses.LINES, curses.COLS // 2, 0, curses.COLS // 2)

        # Changes info display background (for differentiation purposes)
        side_display.bkgd(curses.color_pair(1))
        side_display.refresh()
