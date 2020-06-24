from abc import ABC, abstractmethod


class Term(ABC):
    @abstractmethod
    def get_approx(self):
        return None

    @abstractmethod
    def __str__(self):
        pass
