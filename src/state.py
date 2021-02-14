import sys
import traceback
from typing import (
    List,
    Callable,
    Optional
)


class Context:
    """Represents the current state context"""

    def __init__(self):
        self.current_state = None  # type: Optional[State]
        self.previous_state = None  # type: Optional[State]
        pass

    def get_current_state(self):
        # type: () -> State
        return self.current_state

    def set_current_state(self, state):
        # type: (State) -> None
        self.current_state = state
        pass

    def get_previous_state(self):
        # type: () -> State
        return self.previous_state

    def set_previous_state(self, state):
        # type: (State) -> None
        self.previous_state = state
        pass


class State:
    """Represents a State"""

    def __init__(self, name, *args):
        # type: (str, List[Transition]) -> None
        self.name = name  # type: str
        self.transitions = args  # type: List[Transition]
        pass

    def do_transition(self, context):
        if context.get_current_state() is not None:
            context.set_previous_state(context.get_current_state())
            pass

        context.set_current_state(self)
        active_transition = [t for t in self.transitions if t.is_fulfilled()][0]  # type Optional[Transition]

        if active_transition is not None:
            context.set_current_state(active_transition.get_successor())
            try:
                active_transition.reflex_func()
            except:
                traceback.print_exception(*sys.exc_info())

        pass

    def add_transition(self, transition):
        # type: (Transition) -> None
        """add a transition to transitions of this state"""
        assert isinstance(transition, Transition)
        self.transitions.append(transition)

    def remove_transition(self, transition):
        # type: (Transition) -> None
        """add a transition to transitions of this state"""
        assert isinstance(transition, Transition)
        self.transitions.remove(transition)

    def get_transitions(self):
        # type: () -> List[Transition]
        return self.transitions

    def get_name(self):
        # type: () -> str
        return self.name


class Transition:
    """Represent a Transition from one state to a predecessor state"""

    def __init__(self, predicate, reflex_func, successor):
        # type: (Predicate, Optional[Callable], State) -> None
        assert isinstance(reflex_func, Callable)
        self.predicate = predicate
        self.reflex_func = reflex_func  # type: Optional[Callable]
        self.successor = successor  # type: State
        pass

    def is_fulfilled(self):
        # type: () -> bool
        return self.predicate.test()

    def get_successor(self):
        # type: () -> State
        return self.successor

    def set_successor(self, state):
        # type: (State) -> None
        self.successor = state
        pass


class Predicate:
    """Represent a predicate lambda () -> bool"""

    def __init__(self, a_lambda ):
        # type: (Callable) -> None
        self.a_lambda = a_lambda  # type Callable
        pass

    def test(self):
        # type () -> bool
        return self.a_lambda()

    def _neg(self):
        # type () -> Predicate
        new_lambda = lambda: not self.test()
        return Predicate(new_lambda)

    def _and(self, predicate):
        # type (Predicate) -> Predicate
        new_lambda = lambda: self.a_lambda() and predicate.a_lambda()
        return Predicate(new_lambda)

    def _or(self, predicate):
        # type (Predicate) -> Predicate
        new_lambda = lambda: self.a_lambda() or predicate.a_lambda()
        return Predicate(new_lambda)
