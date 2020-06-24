from termulator_py.terms import Term


class EmptyValue(Term):
    def get_approx(self, variables):
        return None

    def __str__(self):
        return '~'


class Variable(Term):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def get_approx(self, variables):
        return variables.get(self.name)


class Number(Term):
    def __init__(self, number_value):
        self.number_value = number_value

    def __str__(self):
        return str(self.number_value)

    def get_approx(self, variables):
        return self.number_value
