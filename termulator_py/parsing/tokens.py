import string
from abc import ABC, abstractmethod


def start_token(c):
    if c in string.digits:
        return NumberToken()
    if is_operator(c):
        return OperatorToken()
    if c in string.ascii_letters:
        return VariableToken()
    if c in '()':
        return BracketToken()

    if c in string.whitespace:
        return None
    raise ValueError('Cannot start new token with "{}"'.format(c))


def parse_tokens(s):
    tokens = []
    current_token = None

    for c in s:
        if current_token is None:
            current_token = start_token(c)
        elif not current_token.accepts_char(c):
            tokens.append(current_token)
            current_token = start_token(c)

        if current_token is not None:
            current_token.append(c)

    if current_token is not None:
        tokens.append(current_token)

    for token in tokens:
        token.check()

    return tokens


class Token(ABC):
    def __init__(self):
        self.token_chars = []

    @abstractmethod
    def accepts_char(self, c):
        pass

    def append(self, c):
        self.token_chars.append(c)

    def check(self):
        pass

    def __str__(self):
        return type(self).__name__ + '(' + ''.join(self.token_chars) + ')'

    def __repr__(self):
        return str(self)


class NumberToken(Token):
    def __init__(self):
        super().__init__()
        self.got_dot = False

    def accepts_char(self, c):
        if c in string.digits:
            return True
        return (not self.got_dot) and is_number_dot(c) and len(self.token_chars) != 0

    def append(self, c):
        super().append(c)
        if is_number_dot(c):
            self.got_dot = True

    def check(self):
        s = ''.join(self.token_chars)
        if is_number_dot(s[-1]):
            raise ValueError('It is not allowed to end a number with "{}"'.format(s[-1]))


class OperatorToken(Token):
    def __init__(self):
        super().__init__()

    def accepts_char(self, c):
        return is_operator(c) and not self.token_chars

    def check(self):
        if len(self.token_chars) != 1:
            raise ValueError('Got multiple operator signs')


class VariableToken(Token):
    def __init__(self):
        super().__init__()

    def accepts_char(self, c):
        return c in string.ascii_letters or (c in string.digits and self.token_chars)


class BracketToken(Token):
    def __init__(self):
        super().__init__()

    def accepts_char(self, c):
        return c in '()' and not self.token_chars


def is_number_dot(c):
    return c in ['.', ',']


def is_operator(c):
    return c in ['+', '-', '*', '/', '%']
