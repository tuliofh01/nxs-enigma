#! python3

from src.tui.windows.stateful_window import StatefulWindow

if __name__ == "__main__":
    window = StatefulWindow()

    window.run_state("greetings")
    login_state = window.run_state("login")

    if login_state:

    else:
        window.run_state("error")


