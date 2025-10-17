#! python3

from src.tui.windows.empty_window import EmptyWindow

from src.tui.window_transformations.error_state import ErrorState
from src.tui.window_transformations.login_state import LoginState
from src.tui.window_transformations.greetings_state import GreetingsState


class StatefulWindow(EmptyWindow):

    def __init__(self):
        super().__init__()
        self.states = ["greetings", "login", "error"]
        self.current_state = None

    def run_state(self, target_state: str):
        if target_state in self.states:
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



