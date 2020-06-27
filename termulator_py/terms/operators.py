from abc import abstractmethod

from termulator_py.terms import Term
from termulator_py.terms.values import EmptyValue


class InfixOperator(Term):
    @abstractmethod
    def get_operator_priority(self):
        pass

    @abstractmethod
    def get_sub_terms(self):
        pass


class PrefixOperator(Term):
    @abstractmethod
    def get_sub_term(self):
        pass


class Addition(InfixOperator):
    def __init__(self, terms=None):
        self.sub_terms = terms or [EmptyValue()]*2

    def get_sub_terms(self):
        return self.sub_terms

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
        return '+'


class Multiplication(InfixOperator):
    def __init__(self, terms=None):
        self.sub_terms = terms or [EmptyValue()] * 2

    def get_sub_terms(self):
        return self.sub_terms

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
        return '*'


class Negative(PrefixOperator):
    def __init__(self, sub_term):
        self.sub_term = sub_term

    def get_sub_term(self):
        return self.sub_term

    def get_approx(self, variables):
        return -self.sub_term.get_approx()

    def __str__(self):
        return '-'
