#! python3

import enum
from src.tui.windows.empty_window import EmptyWindow
from src.tui.states.error_state import ErrorState
from src.tui.states.login_state import LoginState
from src.tui.states.greetings_state import GreetingsState

class WindowStates(enum.Enum):
    greetings_state = GreetingsState
    login_state = LoginState
    error_state = ErrorState


class StatefulWindow(EmptyWindow):

    def __init__(self):
        super().__init__()
        self.available_states = WindowStates
        self.current_state = None

    def run_state(self, target_state):

        if not isinstance(target_state, WindowStates):
            raise TypeError("target_state must be within WindowStates")
        else:
            self.current_state = target_state.value()




        if target_state is WindowStates:
            for state in self.states:
                if state == self.current_state:
                    match self.current_state:
                        case "greetings":
                            target_state = GreetingsState()
                            target_state.toggle_state(self.main_window)
                        case "login":
                            target_state = LoginState()
                            target_state.toggle_state(self.main_window)
                        case "error":
                            target_state = ErrorState()
                            target_state.toggle_state(self.main_window)
        self.current_state = target_state



