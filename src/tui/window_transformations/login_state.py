#! python3

import curses
import src.misc.config as global_config_variables

from src.tui.windows.empty_window import EmptyWindow
from src.controllers.database_controller import DatabaseCtrl

class LoginState:

    def __init__(self):
        self.db_controller = DatabaseCtrl()
        self.db_path = global_config_variables.DB_FILE_PATH
        self.art = str()
        with open(global_config_variables.LOADING_ART_PATH, "r") as art_characters:
            for character_line in art_characters.readlines():
                self.art += character_line



    def toggle_state(self, target_window: EmptyWindow) -> bool:
        lines = target_window.main_window.getyx()[1]
        columns = target_window.main_window.getyx()[0]

        message = f"PLEASE, INSERT YOUR LOGIN DATA - DEFAULT: \
                  ({global_config_variables.CONFIG["security"]["default_account"]["usr"]},\
                   {global_config_variables.CONFIG["security"]["default_account"]["pwd"]})"
        target_window.main_window.addstr( int( lines * 0.05 ),
                                          int( (columns/2) - (len(message)/2)  ),
                                          message, curses.A_BOLD)

        usr_label = "USERNAME:"
        target_window.main_window.addstr((lines // 4), (columns // 5),
                                          usr_label, curses.A_BOLD)
        pwd_label = "PASSWORD:"
        target_window.main_window.addstr(lines // 3, (columns // 5),
                                         pwd_label, curses.A_BOLD)

        target_window.main_window.move((lines // 4), (columns // 5) + len(usr_label))

        usr_input = str()
        last_char = target_window.main_window.getch()
        positional_counter = 1
        while last_char != ord('\n'):
            if last_char in range(32, 126):
                usr_input = usr_input + chr(last_char)
                target_window.main_window.addstr(lines // 4, (columns // 5)
                              + len(usr_label) + positional_counter, chr(last_char))
                positional_counter += 1
            elif positional_counter == 1:
                pass
            else:
                usr_input = usr_input[:-1]
                positional_counter -= 1
                target_window.main_window.delch(lines // 4, (columns // 5) + len(usr_label) + positional_counter)
            last_char = target_window.main_window.getch()

        target_window.main_window.move((lines // 3), (columns // 5) + len(pwd_label))

        pwd_input = str()
        last_char = target_window.main_window.getch()
        positional_counter = 1
        while last_char != ord('\n'):
            if last_char in range(32, 126):
                pwd_input = pwd_input + chr(last_char)
                target_window.main_window.addstr((lines // 3), (columns // 5) +
                                                 len(pwd_label) + positional_counter, chr(42))
                positional_counter += 1
            elif positional_counter == 1:
                pass
            else:
                pwd_input = pwd_input[:-1]
                positional_counter -= 1
                target_window.main_window.delch((lines // 3), (columns // 5) +
                                                len(pwd_label) + positional_counter)
            last_char = target_window.main_window.getch()

        target_window.main_window.clear()

        target_window.main_window.addstr(
            ((lines / 2) - (9 / 2)),
            ((columns / 2) - int(38 / 2)),
            self.art, curses.color_pair(1)
        )
        curses.flushinp()

        database_ctrl = DatabaseCtrl()
        target_window.main_window.erase()
        target_window.refresh()
        return database_ctrl.authenticate(usr_input, pwd_input)











