from termulator_py.terms import Term


class EmptyValue(Term):
    def get_approx(self):
        return None

    def __str__(self):
        return '~'


class Number(Term):
    def __init__(self, number_value):
        self.number_value = number_value

    def __str__(self):
        return str(self.number_value)

    def get_approx(self):
        return self.number_value
