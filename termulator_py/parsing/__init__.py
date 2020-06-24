from termulator_py.parsing.syntax import to_syntax_tree
from termulator_py.parsing.tokens import parse_tokens


def parse_string(s):
    parsed_tokens = parse_tokens(s)
    tree = to_syntax_tree(parsed_tokens)
    return tree
