from contextlib import suppress

from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext

from states.game_state import GameState
from models.session import GameSession
from new_models.gamer import Gamer
from new_models.pair_session import PairSession
from new_models.matches import Matches
from handlers.callbacks import ReadyCallback, ExitCallback, MyCellCallback
from handlers.callbacks import HitCellCallback, EndCallback
from handlers.keyboards import get_ready_kb, get_exit_kb, get_finish_kb
from handlers.updates import update_other_board, update_my_board

router = Router()


@router.message(Command('start'))
async def cmd_start(
    message: Message,
    state: FSMContext
):
    await state.set_state(GameState.new_game_state)
    await message.answer(
        text=f'Hello, {message.from_user.full_name}'
    )
    await message.answer(
        text=f'* /new_game for a new game session.\n'
            f'* /connect for connecting to an existing session.'
    )
    
    
@router.message(
    GameState.new_game_state,
    Command('new_game')
)
async def cmd_new_game(
    message: Message,
    state: FSMContext,
    matches: Matches
):
    gamer1 = Gamer(message.from_user)
    session = PairSession(gamer1)
    matches.add_gamer(gamer1)
    matches.add_session(session)
    
    await state.set_state(GameState.ready_state)
    
    await message.answer(
        text=f'You created a new game sessions.\n\n'
            'Connection code:'
    )    
    await message.answer(
        text=f'{session.code}'
    )
    
    
@router.message(Command('test'))
async def cmd_test(
    message: Message,
    matches: Matches
):
    all_gamers = '\n'.join(gamer.user.full_name for gamer in matches.gamers)
    all_pairs = '\n'.join(
        f'{id1}: {matches.get_gamer_by_id(id1).player.username}'
        f' vs '
        f'{id2}: {matches.get_gamer_by_id(id2).player.username}'
        for id1, id2 in matches.data
    )
    await message.answer(
        text='all players:\n'
            f'{all_gamers}'
    )
    
    await message.answer(
        text='all_pairs:\n'
            f'{all_pairs}'
    )
    
@router.message(Command('connect'))
async def cmd_connect(
    message: Message,
    state: FSMContext,
    bot: Bot,
    matches: Matches,
    command: CommandObject
):
    code = command.args.strip()
    
    session = matches.get_session_by_code(code)
    
    if not session:
        await message.answer(
            text=f'The code is invalid.\n'
                'Try Again.'
        )
        return
    
    gamer2 = Gamer(message.from_user)
    session.to_pair(gamer2)
    matches.add_match(session)
    matches.add_gamer(gamer2)
    
    user1 = session.gamer1.user
    user1_id = session.gamer1.user.id
    
    await state.set_state(GameState.ready_state)
    
    await message.answer(
        text=f'You and {user1.full_name}({user1.id}) are connected.\n\n'
            f'Press OK to set the boards.',
        reply_markup=get_ready_kb()
    )
    # await bot.send_message(
    #     user1_id,
    #     text='If you ready '
    # )
    
    await bot.send_message(
        chat_id=user1_id,
        text=f'You and {message.from_user.full_name}({message.from_user.id}) are connected.\n\n'
            f'Press OK to set the boards.',
        reply_markup=get_ready_kb()
    )


@router.message(Command('exit'))
async def cmd_exit(
    message: Message,
    state: FSMContext,
    matches: Matches,
    bot: Bot
):
    await state.clear()
    current_gamer = matches.get_gamer_by_id(message.from_user.id)
    opp = matches.get_gamer_opponent_by_id(current_gamer.user.id)
    
    
    matches.delete_match_by_gamer_id(current_gamer.user.id)
    matches.delete_gamer(current_gamer)
    
    await message.answer(
        text='Your game was terminated.',
        reply_markup=get_exit_kb()
    )
    await bot.send_message(
        chat_id=opp.user.id,
        text='Your game was terminated',
        reply_markup=get_exit_kb()
    )


@router.callback_query(
    ExitCallback.filter()
)
async def exit_cb_handler(
    callback: CallbackQuery,
    matches: Matches,
    state: FSMContext,
    bot: Bot
):
    await state.clear()
    await callback.answer()


@router.callback_query(
    GameState.gameplay_state,
    MyCellCallback.filter()
)
async def my_cell_cb_handler(
    callback: CallbackQuery,
    callback_data: MyCellCallback
):
    await callback.answer()

@router.callback_query(
    GameState.ready_state,
    ReadyCallback.filter()
)
async def ready_cb_handler(
    callback: CallbackQuery,
    matches: Matches,
    state: FSMContext,
    bot: Bot
):
    current_user = callback.from_user
    current_gamer = matches.get_gamer_by_id(current_user.id)
    opponent_gamer = matches.get_gamer_opponent_by_id(current_user.id)
    opponent_user = opponent_gamer.user
    
    session = matches.get_game_session_by_gamer(current_gamer)
    
    current_gamer.my_message = await bot.send_message(
        chat_id=current_user.id,
        text=f'🔔               YOUR BOARD               🔔',
        reply_markup=current_gamer.get_my_keyboard()
    )
    
    current_gamer.other_message = await bot.send_message(
        chat_id=current_user.id,
        text=f'🔔      {session.to_move.username}\'s turn      🔔',
        reply_markup=current_gamer.get_other_keyboard()
    )

    await state.set_state(GameState.gameplay_state)
    await callback.answer()
    

    
@router.callback_query(
    GameState.gameplay_state,
    HitCellCallback.filter()
)
async def hit_handle(
    callback: CallbackQuery,
    callback_data: HitCellCallback,
    state: GameState,
    matches: Matches,
    bot: Bot
):
    current_gamer = matches.get_gamer_by_id(callback.from_user.id)
    game_session = matches.get_game_session_by_gamer(current_gamer)
    opponent = matches.get_gamer_opponent_by_id(current_gamer.user.id)
    
    if current_gamer.player is not game_session.to_move:
        await callback.answer()
        return
    
    hit_point = tuple(int(i) for i in callback_data.value.split())
    game_session.move(hit_point[0], hit_point[1])
    
    await update_other_board(current_gamer, game_session)
    await update_my_board(opponent, game_session)
    await update_other_board(opponent, game_session)
    
    if game_session.winner:
        await bot.send_message(
            chat_id=current_gamer.user.id,
            text=f'{game_session.winner.username} WON THE MATCH!!!\n',
            reply_markup=get_finish_kb()
        )
        
        await bot.send_message(
            chat_id=opponent.user.id,
            text=f'{game_session.winner.username} WON THE MATCH!!!\n',
            reply_markup=get_finish_kb()
        )
    
    await callback.answer()
    
    
@router.callback_query(
    GameState.gameplay_state,
    EndCallback.filter()
)
async def finish_cb_handler(
    callback: CallbackQuery,
    state: FSMContext,
    matches: Matches,
    bot: Bot
):
    await state.set_state(GameState.end_state)
    
    current_gamer = matches.get_gamer_by_id(callback.from_user.id)
    opp = matches.get_gamer_opponent_by_id(current_gamer.user.id)
    
    
    matches.delete_match_by_gamer_id(current_gamer.user.id)
    matches.delete_gamer(current_gamer)
    
    await callback.answer()