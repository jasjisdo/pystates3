import unittest

from state import (
    State,
    Predicate,
    Transition,
    Context
)


class StateTestCase(unittest.TestCase):

    def test_state_init(self):
        state = State("TestState")
        self.assertEqual(state.get_name(), "TestState")
        pass

    def test_state_transition(self):
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


if __name__ == '__main__':
    unittest.main()
