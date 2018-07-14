'''There will be a documentation'''

from abc import ABCMeta, abstractmethod


class State(metaclass=ABCMeta):
    @abstractmethod
    def parser_answers(self):
        pass


class Context:
    def __init__(self, state):
        self._state = state


