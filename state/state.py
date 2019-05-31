from typing import List, Callable


class Context:
    """Represents the current state context"""

    current_state = None  # type: State
    previous_state = None  # type: State

    def get_current_state(self):
        # type: () -> State
        return self.current_state

    def set_current_state(self, state):
        # type: (State) -> None
        self.current_state = state
        pass

    def get_previous_state(self):
        # type: () -> State
        return self.current_state

    def set_previous_state(self, state):
        # type: (State) -> None
        self.current_state = state
        pass


class State:
    """Represents a State"""

    name = None  # type: str
    transitions = []  # type: List[Transition]

    def __init__(self, name, transitions):
        # type: (str, List[Transition]) -> None
        self.name = name
        self.transitions = transitions
        pass

    def do_transition(self, context):
        # todo implement this method
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
    """Represent a Transition from one state to a predecessor"""

    predicate = None # type: Callable
    reflex_func = None # type: Callable
    successor = None  # type: State

    def __init__(self, predicate, reflex_func, successor):
        # type: (Predicate, Callable, State) -> None
        self.predicate_lambda = predicate
        pass

    def get_successor(self):
        # type: () -> State
        return self.successor

    def set_successor(self, state):
        # type: (State) -> None
        self.successor = state
        pass


class Predicate:
    """Represent a predicate lambda () -> bool"""
    a_lambda = None  # type Callable

    def __init__(self, a_lambda ):
        # type: (Callable) -> None
        self.a_lambda = a_lambda
        pass

    def test(self):
        # type () -> bool
        return self.a_lambda()

    def _and(self, predicate):
        # type (Predicate) -> Predicate
        new_lambda = lambda: self.a_lambda() and predicate.a_lambda()
        return Predicate(new_lambda)

    def _or(self, predicate):
        # type (Predicate) -> Predicate
        new_lambda = lambda: self.a_lambda() or predicate.a_lambda()
        return Predicate(new_lambda)


if __name__ == '__main__':
    hello = 'Hallo'
    one = 1
    bello = 'Bello'
    zero = 0

    startWithH = lambda text: text.startswith('H')
    greaterZero = lambda number: number > 0

    true_text_predicate = Predicate(lambda: startWithH(hello))
    print(true_text_predicate.test())

    true_number_predicate = Predicate(lambda: greaterZero(one))
    print(true_number_predicate.test())

    true_and_predicate = true_number_predicate._and(true_text_predicate)
    print(true_and_predicate.test())

    false_text_predicate = Predicate(lambda: startWithH(bello))
    print(false_text_predicate.test())

    false_number_predicate = Predicate(lambda: greaterZero(zero))
    print(false_number_predicate.test())

    false_and_predicate = false_number_predicate._and(false_number_predicate)
    print(false_and_predicate.test())
