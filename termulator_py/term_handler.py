from termulator_py.parsing import parse_string


class TermHandler:
    def __init__(self):
        expr = parse_string('1 * 2 * 3 * 4 * 5 * (2+1) + 6 * 7')

        print(expr)
        print(expr.get_approx({'x': 3.1415}))
