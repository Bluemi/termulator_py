from termulator_py.parsing import parse_string


class TermHandler:
    def __init__(self):
        tokens = parse_string('123.45 * 45.0 + 1')
        print(tokens)
