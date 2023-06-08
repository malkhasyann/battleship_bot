'''This module is for states of the FSM'''


from aiogram.fsm.state import StatesGroup, State


class GameState(StatesGroup):
    new_game_state = State()
    gameplay_state = State()
    ready_state = State()
    end_state = State()