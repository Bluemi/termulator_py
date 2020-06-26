from enum import Enum

from termulator_py.terms.operators import Operator
from termulator_py.util import term_iterator, term_cursor_iterator, cursor_contains_cursor, cursor_equals, \
    get_term_by_cursor


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
        self.cursor = []

    def get_top(self, cutoff=0):
        if cutoff == 0:
            indices = self.cursor
        else:
            indices = self.cursor[:-cutoff]

        return get_term_by_cursor(self.term, indices)

    def get_term_iterator(self):
        return term_iterator(self.term)

    def get_print_iterator(self):
        contains = False
        for term, parent, cursor in term_cursor_iterator(self.term):
            if contains:
                if not cursor_contains_cursor(self.cursor, cursor):
                    contains = False
                    yield CursorPosition.ChildEnd
            else:
                if cursor_contains_cursor(self.cursor, cursor):
                    contains = True
                    yield CursorPosition.ChildStart

            cursor_equal = cursor_equals(self.cursor, cursor)
            if cursor_equal:
                yield CursorPosition.CursorStart
            yield term
            if cursor_equal:
                yield CursorPosition.CursorEnd
        if contains:
            yield CursorPosition.ChildEnd

    def go_down(self):
        top = self.get_top()
        if isinstance(top, Operator):
            self.cursor.append(0)
            return True
        return False

    def go_up(self):
        if self.cursor:
            self.cursor.pop()
            return True
        return False

    def go_right(self):
        if self.cursor:
            parent = self.get_top(cutoff=1)
            if self.cursor[-1] + 1 < len(parent.get_sub_terms()):
                self.cursor[-1] += 1
                return True
        return False

    def go_left(self):
        if self.cursor:
            if self.cursor[-1] > 0:
                self.cursor[-1] -= 1
                return True
        return False
