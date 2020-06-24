from termulator_py.terms import Term
from termulator_py.terms.values import EmptyValue


class Addition(Term):
    def __init__(self, terms=None):
        self.sub_terms = terms or [EmptyValue()]*2

    def get_approx(self):
        sum_value = 0
        for sub_term in self.sub_terms:
            if isinstance(sub_term, EmptyValue):
                return EmptyValue()
            sum_value += sub_term.get_approx()

        return sum_value

    def __str__(self):
        return '{} + {}'.format(*self.sub_terms)
