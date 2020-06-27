from enum import Enum

from termulator_py.terms.operators import InfixOperator, PrefixOperator, Operator
from termulator_py.util import print_iterator, cursor_equals, get_term_by_cursor, PrintIteratorFlag, \
    cut_cursor_right


class PrintMetaInfo(Enum):
    ChildStart = 0
    ChildEnd = 1
    CursorStart = 2
    CursorEnd = 3
    BracketStart = 4
    BracketEnd = 5


class TermHandler:
    def __init__(self):
        self.term_handles = []

    def add_term(self, term):
        self.term_handles.append(TermHandle(term))


class TermHandle:
    def __init__(self, term):
        self.term = term
        self.cursor = []

    def get_top(self, cutoff=0):
        return get_term_by_cursor(self.term, cut_cursor_right(self.cursor, cutoff))

    def get_print_iterator(self):
        for term, cursor, flag in print_iterator(self.term):
            if flag == PrintIteratorFlag.TERM:
                cursor_equal = cursor_equals(self.cursor, cursor)
                if cursor_equal:
                    yield PrintMetaInfo.CursorStart
                yield term
                if cursor_equal:
                    yield PrintMetaInfo.CursorEnd
            elif flag == PrintIteratorFlag.ENTER:
                if cursor_equals(self.cursor, cursor):
                    yield PrintMetaInfo.ChildStart
                parent = get_term_by_cursor(self.term, cut_cursor_right(cursor, 1))
                if isinstance(parent, InfixOperator) and isinstance(term, InfixOperator):
                    if parent.get_operator_priority() > term.get_operator_priority():
                        yield PrintMetaInfo.BracketStart
                if isinstance(parent, PrefixOperator) and isinstance(term, InfixOperator):
                    yield PrintMetaInfo.BracketStart
            elif flag == PrintIteratorFlag.LEAVE:
                parent = get_term_by_cursor(self.term, cut_cursor_right(cursor, 1))
                if isinstance(parent, InfixOperator) and isinstance(term, InfixOperator):
                    if parent.get_operator_priority() > term.get_operator_priority():
                        yield PrintMetaInfo.BracketEnd
                if isinstance(parent, PrefixOperator) and isinstance(term, InfixOperator):
                    yield PrintMetaInfo.BracketEnd
                if cursor_equals(self.cursor, cursor):
                    yield PrintMetaInfo.ChildEnd

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
            if isinstance(parent, InfixOperator):
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
