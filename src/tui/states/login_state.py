#! python3

import curses

from src.tui.states.default_state import DefaultState
from src.tui.windows.stateful_window import StatefulWindow
from src.controllers.database_controller import DatabaseCtrl

class LoginState(DefaultState):

    def __init__(self, target_window: StatefulWindow):
        super().__init__()

        # Core objs initialization
        self.state_controller = DatabaseCtrl()
        self.application_window_obj = target_window
        self.application_window_interface = self.application_window_obj.main_window

        # ASCII art objs initialization
        self.ascii_art_obj = str()
        self.ascii_art_path = self.environmental_references.LOADING_ART_PATH
        with open(self.ascii_art_path, "r") as text_file:
            for line in text_file.readlines():
                self.ascii_art_obj += line

    def toggle_self(self) -> bool:
        # Cartesian basal references
        cols = self.application_window_interface.getyx()[0]
        lines = self.application_window_interface.getyx()[1]

        # Rendering interface elements
        login_prompt = f"PLEASE, INSERT YOUR LOGIN DATA - DEFAULT: \
                  ({self.environmental_references.CONFIG["security"]["default_account"]["usr"]},\
                   {self.environmental_references.CONFIG["security"]["default_account"]["pwd"]})"
        self.application_window_interface.addstr(int( lines * 0.05 ), int((cols/2) - (len(login_prompt)/2)),
                                                 login_prompt, curses.A_BOLD)
        usr_label = "USERNAME:"
        self.application_window_interface.addstr((lines // 4), (cols // 5),
                                                  usr_label, curses.A_BOLD)
        pwd_label = "PASSWORD:"
        self.application_window_interface.addstr((lines // 3), (cols // 5),
                                                  pwd_label, curses.A_BOLD)

        # Positioning cursor
        self.application_window_interface.move((lines // 4), (cols // 5) + len(usr_label))

        # Fetching and rendering textual input
        usr_input = str()
        last_char = self.application_window_interface.getch()
        positional_counter = 1
        while last_char != ord('\n'):
            if (last_char in range(32, 126)) or (positional_counter == 1):
                usr_input = usr_input + chr(last_char)
                self.application_window_interface.addstr((lines // 4),
                                                         ((cols // 5) + len(usr_label) + positional_counter),
                                                         chr(last_char))
                positional_counter += 1
            else:
                usr_input = usr_input[:-1]
                positional_counter -= 1
                self.application_window_interface.delch(lines // 4,
                                                        (cols // 5) + len(usr_label) + positional_counter)
            last_char = self.application_window_interface.getch()

        # Positioning cursor
        self.application_window_interface.move((lines // 3), (cols // 5) + len(pwd_label))

        # Fetching and rendering sensitive textual input
        pwd_input = str()
        last_char = self.application_window_interface.getch()
        positional_counter = 1
        while last_char != ord('\n'):
            if last_char in range(32, 126) or positional_counter == 1:
                pwd_input = pwd_input + chr(last_char)
                self.application_window_interface.addstr((lines // 3),
                                                         (cols // 5) + len(pwd_label) + positional_counter,
                                                         chr(42))
                positional_counter += 1
            else:
                pwd_input = pwd_input[:-1]
                positional_counter -= 1
                self.application_window_interface.delch((lines // 3),
                                                        (cols // 5) + len(pwd_label) + positional_counter)
            last_char = self.application_window_interface.getch()

        # Rendering loading screen
        self.application_window_interface.clear()
        self.application_window_interface.addstr(
            ((lines / 2) - (9 / 2)),
            ((cols / 2) - int(38 / 2)),
            self.ascii_art_obj,
            curses.color_pair(10)
        )
        curses.flushinp()

        # Database interaction
        db_handler = DatabaseCtrl()
        self.application_window_interface.erase()
        self.application_window_interface.refresh()
        status = db_handler.authenticate(usr_input, pwd_input)
        if not status:
            raise ValueError("Authentication failed!")
        return status











