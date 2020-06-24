class EmptyValue:
    def __str__(self):
        return '~'


class Number:
    def __init__(self, number_value):
        self.number_value = number_value

    def __str__(self):
        return str(self.number_value)
