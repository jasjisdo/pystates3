import time
import schedule
import constants

from states import StateRed, StateYellow, StateGreen
from state import Transition, Predicate


def init_traffic_light():
    state_red = StateRed()
    state_yellow = StateYellow()
    state_green = StateGreen()

    constants.CONTEXT.set_current_state(state_red)

    red_to_green = Transition(
        predicate=Predicate(
            lambda: constants.CONTEXT.get_current_state().get_name() == StateRed.name),
        reflex_func=lambda: print("switch from red to green light"),
        successor=state_green
    )
    green_to_yellow = Transition(
        predicate=Predicate(
            lambda: constants.CONTEXT.get_current_state().get_name() == StateGreen.name),
        reflex_func=lambda: print("switch from green to yellow light"),
        successor=state_yellow
    )
    yellow_to_red = Transition(
        predicate=Predicate(
            lambda: constants.CONTEXT.get_current_state().get_name() == StateYellow.name),
        reflex_func=lambda: print("switch from yellow to red light"),
        successor=state_red
    )

    state_red.add_transition(red_to_green)
    state_yellow.add_transition(yellow_to_red)
    state_green.add_transition(green_to_yellow)

    pass


def switch_lights():
    if constants.EXECS <= 0:
        return schedule.CancelJob
    constants.CONTEXT.get_current_state().do_transition(constants.CONTEXT)
    constants.EXECS -= 1
    pass


if __name__ == '__main__':
    init_traffic_light()
    schedule.every(3).seconds.do(switch_lights)

    while constants.EXECS > 0:
        schedule.run_pending()
        time.sleep(1)
