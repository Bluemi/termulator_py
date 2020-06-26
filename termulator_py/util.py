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


def term_cursor_iterator(term):
    return _term_cursor_iterator_impl(term, [])


def _term_cursor_iterator_impl(term, cursor):
    if isinstance(term, Operator):
        # iterate over all sub terms except the last
        for index, sub_term in enumerate(term.get_sub_terms()[:-1]):
            if isinstance(sub_term, Operator):
                if sub_term.get_operator_priority() < term.get_operator_priority():
                    yield None, '('
            sub_cursor = [*cursor, index]
            for sub_sub_cursor, sub_sub_term in _term_cursor_iterator_impl(sub_term, sub_cursor):
                yield sub_sub_cursor, sub_sub_term
            yield cursor, term
            if isinstance(sub_term, Operator):
                if sub_term.get_operator_priority() < term.get_operator_priority():
                    yield None, ')'
        # handle last term
        if term.get_sub_terms():
            last_index = len(term.get_sub_terms()) - 1
            sub_cursor = [*cursor, last_index]
            sub_term = term.get_sub_terms()[-1]
            if isinstance(sub_term, Operator):
                if sub_term.get_operator_priority() < term.get_operator_priority():
                    yield None, '('
            for sub_sub_cursor, sub_sub_term in _term_cursor_iterator_impl(sub_term, sub_cursor):
                yield sub_sub_cursor, sub_sub_term
            if isinstance(sub_term, Operator):
                if sub_term.get_operator_priority() < term.get_operator_priority():
                    yield None, ')'
    else:
        yield cursor, term


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
