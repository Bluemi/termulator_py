import curses
import string
from enum import Enum

from termulator_py.parsing import parse_string
from termulator_py.term_handler import TermHandler


PRINTABLE_CH = [ord(key) for key in string.printable]


class DisplayMode(Enum):
    TERMS = 0
    CONSOLE = 1


class Console:
    def __init__(self):
        self.command = []

    def get_command(self):
        return ''.join(self.command)

    def handle_ch(self, ch):
        if ch in PRINTABLE_CH:
            self.command.append(chr(ch))

    def clear_command(self):
        self.command = []


class MainManager:
    def __init__(self, window, messages):
        self.window = window
        self.term_handler = TermHandler()
        self.display_mode = DisplayMode.TERMS
        self.term_handler.add_term(parse_string('1 + 2 * 3'))
        self.console = Console()
        self.running = True
        self.messages = messages

    def run(self):
        while self.running:
            self.window.clear()
            self.render()
            self.window.refresh()
            ch = self.window.getch()
            self.handle_ch(ch)

    def render(self):
        self.update_terms()
        if self.display_mode == DisplayMode.TERMS:
            pass
        elif self.display_mode == DisplayMode.CONSOLE:
            self.window.addstr(curses.LINES-1, 0, ':{}'.format(self.console.get_command()))

    def update_terms(self):
        for y, term_string in enumerate(self.term_handler.get_string_representations()):
            self.window.addstr(y, 0, term_string)

    def handle_ch(self, ch):
        if self.display_mode == DisplayMode.CONSOLE:
            if ch == 27:  # ESCAPE
                self.display_mode = DisplayMode.TERMS
            elif ch == 10:  # ENTER
                self.execute_command(self.console.get_command())
                self.console.clear_command()
                self.display_mode = DisplayMode.TERMS
            else:
                self.console.handle_ch(ch)
        elif self.display_mode == DisplayMode.TERMS:
            if ch == ord('q'):
                self.running = False
            elif ch == ord(':'):
                self.display_mode = DisplayMode.CONSOLE

    def log(self, message):
        self.messages.append(message)

    def execute_command(self, command):
        if command == 'quit' or command == 'q':
            self.running = False


def start_app(window: curses.window, messages):
    window.keypad(False)

    main_manager = MainManager(window, messages)
    main_manager.run()


def main():
    messages = []
    try:
        curses.wrapper(start_app, messages)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        raise e
    finally:
        for message in messages:
            print(message)


if __name__ == '__main__':
    main()
