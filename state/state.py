from typing import List


class State:
    """Represents a State"""

    name = None  # type: str
    transitions = []  # type: List[Transition]

    def __init__(self, name):
        self.name = name
        pass

    def do_transition(self, context):
        # todo implement this method
        pass

    def add_transition(self, transition):
        # type: (Transition) -> None
        """add a transition to transitions of this state"""
        assert isinstance(transition, Transition)
        self.transitions.append(transition)


class Transition:
    """Represent a Transition from one state to an another"""

    is_fulfilled = False  # type: bool
    successor = None  # type: State

    def __init__(self):
        self.is_fulfilled = False

    def set_successor(self, state):
        # type: (State) -> None
        self.successor = state

    def get_successor(self):
        return self.successor
