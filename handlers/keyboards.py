from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from handlers.callbacks import ReadyCallback, ExitCallback, EndCallback


def get_ready_kb():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='OK',
        callback_data=ReadyCallback()
    )
    
    return builder.as_markup()

def get_exit_kb():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='OK',
        callback_data=ExitCallback()
    )
    
    return builder.as_markup()


def get_finish_kb():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='OK',
        callback_data=EndCallback()
    )
    
    return builder.as_markup()