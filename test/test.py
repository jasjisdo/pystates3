import unittest

from state.state import Context, State, Predicate, Transition


class TestContext(unittest.TestCase):

    context = None  # type: Context
    start_state = None  # type: State
    end_state = None  # type: State
    transition = None  # type: Transition

    def setUp(self):
        self.start_state = State('start')
        self.end_state = State('end')
        self.transition = Transition(Predicate(lambda: True), successor=self.end_state)
        self.start_state.add_transition(self.transition)
        self.context = Context()
        self.context.set_current_state(self.start_state)
        pass

    def tearDown(self):
        self.context = Context()
        self.start_state = None
        self.end_state = None
        self.transition = None

    def test_1(self):
        self.context.set_current_state(self.start_state)
        self.assertEquals(self.start_state, self.context.get_current_state(), 'previous state is unequals start state')

    def test_2(self):
        self.context.set_previous_state(self.start_state)
        self.assertEquals(self.start_state, self.context.get_previous_state(), 'previous state is unequals start state')

    def test_3(self):
        self.start_state.do_transition(self.context)
        self.assertIs(self.context.get_previous_state(), self.start_state)
        self.assertIs(self.context.get_current_state(), self.end_state)


class TestState(unittest.TestCase):

    start_state = None  # type: State
    end_state = None  # type: State
    transition = None  # type: Transition

    def setUp(self):
        self.start_state = State('start')
        self.end_state = State('end')
        self.transition = Transition(Predicate(lambda: True), successor=self.end_state)
        self.start_state.add_transition(self.transition)
        pass

    def tearDown(self):
        self.start_state = None
        self.end_state = None
        self.transition = None

    def test_1(self):
        self.assertIsNot(self.start_state, self.end_state, 'state state is equals end state!')

    def test_2(self):
        self.assertEquals('start', self.start_state.name, 'state name is not \'start\'')

    def test_21(self):
        self.assertEquals('start', self.start_state.get_name(), 'state name is not \'start\'')

    def test_3(self):
        self.assertIsNot(self.end_state.transitions, self.start_state.transitions)

    def test_4(self):
        self.assertEquals(self.end_state.transitions, [])

    def test_5(self):
        self.assertIs(self.end_state.get_transitions(), self.end_state.transitions)

    def test_6(self):
        self.start_state.remove_transition(self.transition)
        self.assertEquals(self.end_state.transitions, [])

    def test_7(self):
        self.end_state = State('end', [self.transition])
        self.assertEquals(self.end_state.get_transitions(), [self.transition])

    def test_8(self):
        self.transition.set_successor(self.start_state)
        self.assertEquals(self.transition.get_successor(), self.start_state)


# class Test_WhenCurrentStateIsSet_ThenGetCurrentStateIsLikeExpected(unittest.TestCase):
#
#     context = None
#     start_state = None
#
#     def setUp(self):
#         self.context = Context()
#         self.start_state = State('start')
#
#     def test(self):
#         self.context.set_current_state(self.start_state)
#         self.assertEquals(self.start_state, self.context.get_current_state(), 'current state is unequals start state')