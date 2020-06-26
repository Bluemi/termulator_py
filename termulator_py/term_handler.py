from enum import Enum

from termulator_py.terms.operators import Operator
from termulator_py.util import term_iterator, term_cursor_iterator, cursor_contains_cursor, cursor_equals


class CursorPosition(Enum):
    ChildStart = 0
    ChildEnd = 1
    CursorStart = 2
    CursorEnd = 3


class TermHandler:
    def __init__(self):
        self.term_handles = []

    def add_term(self, term):
        self.term_handles.append(TermHandle(term))

    def get_string_representations(self):
        return map(
            lambda terms: ' '.join(map(str, terms)),
            map(
                TermHandle.get_term_iterator,
                self.term_handles
            )
        )


class TermHandle:
    def __init__(self, term):
        self.term = term
        self.indices = []

    def get_top(self, term, cutoff=0):
        if cutoff == 0:
            indices = self.indices
        else:
            indices = self.indices[:-cutoff]
        for i in indices:
            if isinstance(term, Operator):
                sub_terms = term.get_sub_terms()
                if len(sub_terms) < i:
                    term = sub_terms[i]
        return term

    def get_term_iterator(self):
        return term_iterator(self.term)

    def get_cursor_iterator(self):
        contains = False
        for cursor, term in term_cursor_iterator(self.term):
            if contains:
                if not self.contains_cursor(cursor):
                    contains = False
                    yield CursorPosition.ChildEnd
            else:
                if self.contains_cursor(cursor):
                    contains = True
                    yield CursorPosition.ChildStart

            if cursor_equals(self.indices, cursor):
                yield CursorPosition.CursorStart
                yield term
                yield CursorPosition.CursorEnd
            else:
                yield term
        if contains:
            yield CursorPosition.ChildEnd

    def contains_cursor(self, cursor):
        return cursor_contains_cursor(self.indices, cursor)

    def go_down(self):
        top = self.get_top(self.term)
        if isinstance(top, Operator):
            self.indices.append(0)
            return True
        return False

    def go_up(self):
        if self.indices:
            self.indices.pop()
            return True
        return False

    def go_right(self):
        if self.indices:
            parent = self.get_top(self.term, cutoff=1)
            if self.indices[-1] + 1 < len(parent.get_sub_terms()):
                self.indices[-1] += 1
                return True
        return False

    def go_left(self):
        if self.indices:
            if self.indices[-1] > 0:
                self.indices[-1] -= 1
                return True
        return False
