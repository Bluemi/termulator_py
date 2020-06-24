import time
from curses import wrapper as curses_wrapper

from termulator_py.term_handler import TermHandler


def main(_curses_window):
    term_handler = TermHandler()
    # time.sleep(2)


if __name__ == '__main__':
    # curses_wrapper(main)
    main(None)
