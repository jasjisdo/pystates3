from state import State, Transition

EXECS = 9
/1/


class StateRed(State):

    name = "Red traffic light"

    def __init__(self, *args: Transition) -> None:
        super().__init__(StateRed.name, *args)

    pass


class StateYellow(State):

    name = "Yellow traffic light"

    def __init__(self, *args: Transition) -> None:
        super().__init__(StateYellow.name, *args)

    pass


class StateGreen(State):

    name = "Green traffic light"

    def __init__(self, *args: Transition) -> None:
        super().__init__(StateGreen.name, *args)

    pass
