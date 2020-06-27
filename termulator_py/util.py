from enum import Enum

from termulator_py.terms.operators import Operator


def term_iterator(term):
    if isinstance(term, Operator):
        # iterate over all sub terms except the last
        for sub_term in term.get_sub_terms()[:-1]:
            for sub_sub_term in term_iterator(sub_term):
                yield sub_sub_term
            yield term
        # handle last term
        if term.get_sub_terms():
            for sub_sub_term in term_iterator(term.get_sub_terms()[-1]):
                yield sub_sub_term
    else:
        yield term


class PrintIteratorFlag(Enum):
    ENTER = 0
    LEAVE = 1
    TERM = 2


def print_iterator(term):
    return _print_iterator_impl(term, [])


def _print_iterator_impl(term, cursor):
    yield term, cursor, PrintIteratorFlag.ENTER
    if isinstance(term, Operator):
        last_index = len(term.get_sub_terms()) - 1
        for index, sub_term in enumerate(term.get_sub_terms()):
            sub_cursor = [*cursor, index]
            for sub_sub_term, sub_sub_cursor, flag in _print_iterator_impl(sub_term, sub_cursor):
                yield sub_sub_term, sub_sub_cursor, flag
            if index != last_index:
                yield term, cursor, PrintIteratorFlag.TERM
    else:
        yield term, cursor, PrintIteratorFlag.TERM
    yield term, cursor, PrintIteratorFlag.LEAVE


def cursor_contains_cursor(base, cursor):
    if len(base) > len(cursor):
        return False
    for base_index, cursor_index in zip(base, cursor):
        if base_index != cursor_index:
            return False
    return True


def cursor_equals(cursor0, cursor1):
    if len(cursor0) != len(cursor1):
        return False
    for index0, index1 in zip(cursor0, cursor1):
        if index0 != index1:
            return False
    return True


def get_term_by_cursor(term, cursor):
    for i in cursor:
        if isinstance(term, Operator):
            sub_terms = term.get_sub_terms()
            if i < len(sub_terms):
                term = sub_terms[i]
            else:
                return None
        else:
            return None
    return term


def cut_cursor_right(cursor, cutoff):
    if cutoff == 0:
        return cursor
    return cursor[:-cutoff]
