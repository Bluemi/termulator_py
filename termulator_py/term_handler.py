class TermHandler:
    def __init__(self):
        self.root_terms = []

    def add_term(self, term):
        self.root_terms.append(term)

    def get_string_representations(self):
        return list(map(str, self.root_terms))
