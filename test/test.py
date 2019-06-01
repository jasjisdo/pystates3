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


class TestTransition(unittest.TestCase):

    transition1 = None  # type: Transition
    transition2 = None  # type: Transition
    end_state = None  # type: State

    def setUp(self):
        self.end_state = State('end')
        self.transition1 = Transition(Predicate(lambda: True), successor=self.end_state)
        self.transition2 = Transition(Predicate(lambda: False), successor=self.end_state)

    def tearDown(self):
        self.transition1 = None
        self.end_state = None

    def test_1(self):
        self.assertIsNotNone(self.transition1.get_successor())
        self.assertIs(self.transition1.get_successor(), self.end_state)

    def test_2(self):
        self.assertTrue(self.transition1.is_fulfilled())
        self.assertFalse(self.transition2.is_fulfilled())


class TestPredicate(unittest.TestCase):

    true_text_predicate = None  # type: Predicate
    true_number_predicate = None  # type: Predicate
    true_and_predicate = None  # type: Predicate
    true_or_predicate = None  # type: Predicate
    false_text_predicate = None  # type: Predicate
    false_number_predicate = None  # type: Predicate
    false_and_predicate = None  # type: Predicate
    false_or_predicate = None  # type: Predicate

    def setUp(self):
        hello = 'Hallo'
        one = 1
        bello = 'Bello'
        zero = 0
        startWithH = lambda text: text.startswith('H')
        greaterZero = lambda number: number > 0
        self.true_text_predicate = Predicate(lambda: startWithH(hello))
        self.true_number_predicate = Predicate(lambda: greaterZero(one))
        self.true_and_predicate = self.true_number_predicate._and(self.true_text_predicate)
        self.false_text_predicate = Predicate(lambda: startWithH(bello))
        self.false_number_predicate = Predicate(lambda: greaterZero(zero))
        self.false_and_predicate = self.false_number_predicate._and(self.false_number_predicate)
        self.true_or_predicate = self.true_number_predicate._or(self.false_text_predicate)
        self.false_or_predicate = self.false_number_predicate._or(self.false_text_predicate)

    def tearDown(self):
        self.true_text_predicate = None
        self.true_number_predicate = None
        self.true_and_predicate = None
        self.true_or_predicate = None
        self.false_text_predicate = None
        self.false_number_predicate = None
        self.false_and_predicate = None
        self.false_or_predicate = None

    def test_1(self):
        self.assertIsNotNone(self.true_text_predicate.a_lambda)
        self.assertIsNotNone(self.true_number_predicate.a_lambda)
        self.assertIsNotNone(self.true_and_predicate.a_lambda)
        self.assertIsNotNone(self.true_or_predicate.a_lambda)
        self.assertIsNotNone(self.false_text_predicate.a_lambda)
        self.assertIsNotNone(self.false_number_predicate.a_lambda)
        self.assertIsNotNone(self.false_and_predicate.a_lambda)
        self.assertIsNotNone(self.false_or_predicate.a_lambda)

    def test_2(self):
        self.assertTrue(self.true_text_predicate.test())
        self.assertTrue(self.true_number_predicate.test())
        self.assertTrue(self.true_and_predicate.test())
        self.assertTrue(self.true_or_predicate.test())
        self.assertFalse(self.false_text_predicate.test())
        self.assertFalse(self.false_number_predicate.test())
        self.assertFalse(self.false_and_predicate.test())
        self.assertFalse(self.false_or_predicate.test())

