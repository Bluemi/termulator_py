from termulator_py.parsing.tokens import BracketToken, OperatorToken, VariableToken, NumberToken
from termulator_py.terms import Term
from termulator_py.terms.operators import Addition, Multiplication
from termulator_py.terms.values import Number, Variable


def tokens_to_syntax_tree(tokens):
    while True:
        left, right = get_bracket_indices(tokens)
        if (left is None) or (right is None):
            break
        else:
            tokens_before_left = tokens[:left]
            tokens_between = tokens[left+1: right]
            tokens_after_right = tokens[right+1:]
            expression = tokens_to_syntax_tree(tokens_between)
            tokens = [*tokens_before_left, expression, *tokens_after_right]

    operator_index = get_lowest_priority_operator(tokens)
    if operator_index is not None:
        operator_left = tokens_to_syntax_tree(tokens[:operator_index])
        operator_right = tokens_to_syntax_tree(tokens[operator_index+1:])
        return operator_to_expression(
            tokens[operator_index],
            operator_left,
            operator_right
        )

    if len(tokens) != 1:
        raise ValueError('Found tokens without operator: {}'.format(tokens))

    token = tokens[0]
    if isinstance(token, VariableToken):
        return Variable(token.get_name())
    elif isinstance(token, NumberToken):
        return Number(token.to_number())
    elif isinstance(token, Term):
        return token
    else:
        raise TypeError('Unexpected token {}'.format(token))


def operator_to_expression(operator, left_expression, right_expression):
    operator_str = operator.get_operator()
    if operator_str == '+':
        return Addition([left_expression, right_expression])
    elif operator_str == '*':
        return Multiplication([left_expression, right_expression])
    else:
        raise NotImplementedError('')


def get_lowest_priority_operator(tokens):
    lowest_operator_index = None
    lowest_operator_priority = None
    for index, token in enumerate(tokens):
        if isinstance(token, OperatorToken):
            if lowest_operator_priority is None or (token.get_operator_priority() <= lowest_operator_priority):
                lowest_operator_index = index
                lowest_operator_priority = token.get_operator_priority()

    return lowest_operator_index


def get_bracket_indices(tokens):
    bracket_counter = 0
    left_bracket_index = None
    right_bracket_index = None
    for index, token in enumerate(tokens):
        if isinstance(token, BracketToken):
            if token.is_left():
                if left_bracket_index is None:
                    left_bracket_index = index
                bracket_counter += 1
            else:
                bracket_counter -= 1
                if bracket_counter < 0:
                    raise ValueError('Found superfluous right bracket')
                if bracket_counter == 0 and right_bracket_index is None:
                    right_bracket_index = index
                    break
    if bracket_counter != 0:
        raise ValueError('Found unclosed left bracket')
    return left_bracket_index, right_bracket_index
