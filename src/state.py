from __future__ import annotations

import logging

from typing import (
    List,
    Callable,
    Optional
)


class Context:
    """Represents the current state context"""

    def __init__(self):
        self.current_state: Optional[State] = None
        self.previous_state: Optional[State] = None
        pass

    def get_current_state(self) -> State:
        return self.current_state

    def set_current_state(self, state: State) -> None:
        self.current_state = state
        pass

    def get_previous_state(self) -> State:
        return self.previous_state

    def set_previous_state(self, state: State) -> None:
        self.previous_state = state
        pass


class State:
    """Represents a State"""

    def __init__(self, name: str, *args: Transition) -> None:
        self.name: str = name
        self.transitions: List[Transition] = list(args)
        pass

    def do_transition(self, context: Context) -> None:
        if context.get_current_state() is not None:
            context.set_previous_state(context.get_current_state())
            pass

        context.set_current_state(self)
        active_transition = [t for t in self.transitions if t.is_fulfilled()][0]

        if active_transition is not None:
            context.set_current_state(active_transition.get_successor())
            try:
                active_transition.reflex_func()
            except Exception as e:
                logging.exception(e)

        pass

    def add_transition(self, transition: Transition) -> None:
        """add a transition to transitions of this state"""
        assert isinstance(transition, Transition)
        self.transitions.append(transition)

    def remove_transition(self, transition: Transition) -> None:
        """add a transition to transitions of this state"""
        assert isinstance(transition, Transition)
        self.transitions.remove(transition)

    def get_transitions(self) -> List[Transition]:
        return self.transitions

    def get_name(self) -> str:
        return self.name


class Transition:
    """Represent a Transition from one state to a predecessor state"""

    def __init__(self,
                 predicate: Predicate,
                 reflex_func: Optional[Callable],
                 successor: State) -> None:
        assert isinstance(reflex_func, Callable)
        self.predicate: Predicate = predicate
        self.reflex_func: Optional[Callable] = reflex_func
        self.successor: State = successor
        pass

    def is_fulfilled(self) -> bool:
        return self.predicate.test()

    def get_successor(self) -> State:
        return self.successor

    def set_successor(self, state: State) -> None:
        self.successor = state
        pass


class Predicate:
    """Represent a predicate lambda () -> bool"""

    def __init__(self, a_lambda: Callable) -> None:
        self.a_lambda = a_lambda
        pass

    def test(self) -> bool:
        return self.a_lambda()

    def _neg(self) -> Predicate:
        def new_lambda(): return not self.test()
        return Predicate(new_lambda)

    def _and(self, predicate: Predicate) -> Predicate:
        def new_lambda(): return self.a_lambda() and predicate.a_lambda()
        return Predicate(new_lambda)

    def _or(self, predicate: Predicate) -> Predicate:
        def new_lambda(): return self.a_lambda() or predicate.a_lambda()
        return Predicate(new_lambda)
