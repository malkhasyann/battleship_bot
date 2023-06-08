from contextlib import suppress

from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from states.game_state import GameState
from models.session import GameSession
from new_models.gamer import Gamer
from new_models.pair_session import PairSession
from new_models.matches import Matches
from handlers.callbacks import ReadyCallback, ExitCallback
from handlers.callbacks import HitCellCallback
from handlers.keyboards import get_ready_kb, get_exit_kb


async def update_other_board(
    gamer: Gamer,
    game_session: GameSession
):
    with suppress(TelegramBadRequest):
        await gamer.other_message.edit_reply_markup(
            reply_markup=gamer.get_other_keyboard()
        )
        
    with suppress(TelegramBadRequest):
        await gamer.other_message.edit_text(
            text=f'🔔      {game_session.to_move.username}\'s turn      🔔',
            reply_markup=gamer.get_other_keyboard()
        )
    
async def update_my_board(
    gamer: Gamer,
    game_session: GameSession
):
    with suppress(TelegramBadRequest):
        await gamer.my_message.edit_reply_markup(
            reply_markup=gamer.get_my_keyboard()
        )