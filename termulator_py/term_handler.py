from termulator_py.parsing import parse_string


class TermHandler:
    def __init__(self):
        expr = parse_string('123.45 * 45.0 + x')

        print(expr)
        print(expr.get_approx({'x': 3.1415}))
