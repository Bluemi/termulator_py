from termulator_py.parsing import parse_string


class TermHandler:
    def __init__(self):
        expr = parse_string('3 * (2 + 3) * 4')

        print(expr)
        print(expr.get_approx({'x': 3.1415}))
