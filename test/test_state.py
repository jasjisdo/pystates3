import unittest

from state import (
    State,
    Predicate,
    Transition,
    Context
)


class StateTestCase(unittest.TestCase):

    def test_given_state_when_init_then_state_name_is_correct(self):
        state = State("TestState")
        self.assertEqual(state.get_name(), "TestState")
        pass

    def test_given_states_with_transitions_when_init_then_transitions_are_correct(self):
        end_state = State("EndState")
        transition1 = Transition(
            Predicate(lambda: True),
            lambda: print("Hello Reflex"),
            end_state
        )
        transition2 = Transition(
            Predicate(lambda: False),
            lambda: print("Hello NOP"),
            end_state
        )
        state: State = State("TestState", transition1, transition2)
        self.assertListEqual(state.transitions, [transition1, transition2])
        pass

    def test_given_transition_from_start_to_end_when_state_transition_then_end_state(self):
        end_state = State("EndState")
        transition = Transition(
            Predicate(lambda: True),
            lambda: print("Hello Reflex"),
            end_state
        )
        start_state = State("StartState", transition)
        context = Context()
        context.set_current_state(start_state)
        start_state.do_transition(context)
        self.assertEqual(context.get_current_state(), end_state)
        self.assertEqual(context.get_previous_state(), start_state)
        pass

    def test_given_when_then_1(self):
        predicates = [Predicate(lambda: True),
                      Predicate(lambda: False)]
        actual = [p._neg().test() for p in predicates]
        expected = [False, True]
        self.assertEqual(expected, actual)
        pass

    def test_given_when_then_2(self):
        predicates = [(Predicate(lambda: True),
                      Predicate(lambda: True)),
                      (Predicate(lambda: True),
                       Predicate(lambda: False)),
                      (Predicate(lambda: False),
                       Predicate(lambda: True)),
                      (Predicate(lambda: False),
                       Predicate(lambda: False))]
        actual = [t[0]._and(t[1]).test() for t in predicates]
        expected = [True, False, False, False]
        self.assertEqual(expected, actual)
        pass

    def test_given_when_then_3(self):
        predicates = [(Predicate(lambda: True),
                       Predicate(lambda: True)),
                      (Predicate(lambda: True),
                       Predicate(lambda: False)),
                      (Predicate(lambda: False),
                       Predicate(lambda: True)),
                      (Predicate(lambda: False),
                       Predicate(lambda: False))]
        actual = [t[0]._or(t[1]).test() for t in predicates]
        expected = [True, True, True, False]
        self.assertEqual(expected, actual)
        pass


if __name__ == '__main__':
    unittest.main()
