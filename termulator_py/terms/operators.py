from abc import abstractmethod

from termulator_py.terms import Term
from termulator_py.terms.values import EmptyValue


class Operator(Term):
    @abstractmethod
    def get_operator_priority(self):
        pass


class Addition(Operator):
    def __init__(self, terms=None):
        self.sub_terms = terms or [EmptyValue()]*2

    def get_operator_priority(self):
        return 0

    def get_approx(self, variables):
        sum_value = 0
        for sub_term in self.sub_terms:
            if isinstance(sub_term, EmptyValue):
                return EmptyValue()
            sum_value += sub_term.get_approx(variables)

        return sum_value

    def __str__(self):
        return join_with_brackets('+', self.sub_terms, self.get_operator_priority())


class Multiplication(Operator):
    def __init__(self, terms=None):
        self.sub_terms = terms or [EmptyValue()] * 2

    def get_operator_priority(self):
        return 1

    def get_approx(self, variables):
        prod_value = 1
        for sub_term in self.sub_terms:
            if isinstance(sub_term, EmptyValue):
                return EmptyValue()
            prod_value *= sub_term.get_approx(variables)

        return prod_value

    def __str__(self):
        return join_with_brackets('*', self.sub_terms, self.get_operator_priority())


def join_with_brackets(sep, terms, own_operator_priority):
    def _bracket_if_necessary(term):
        if isinstance(term, Operator):
            if term.get_operator_priority() < own_operator_priority:
                return '({})'.format(term)
        return str(term)
    return sep.join(map(_bracket_if_necessary, terms))
