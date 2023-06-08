import random
import string

from aiogram.types import User, Message, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from models.player import Player
from handlers.callbacks import MyCellCallback, HitCellCallback


def generate_key():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(8))


cell_mask = {0: '🌊', 1: '🚢', 2: '❌', 3: '💥', 4: '🔥', 5: '▫️'} 



class Gamer:
    def __init__(self, user: User):
        self.user: User = user
        self.player: Player = Player(user.full_name)
        self.my_message: Message = None
        self.other_message: Message = None
        
    def get_my_keyboard(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        board_matrix = self.player.my_board.data
        for i in range(len(board_matrix)):
            for j in range(len(board_matrix)):
                builder.button(
                    text=cell_mask[board_matrix[i][j]],
                    callback_data=MyCellCallback(value=f'{i} {j}')
                )
                
        return builder.as_markup()
    
    def get_other_keyboard(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        board_matrix = self.player.other_board.data
        for i in range(len(board_matrix)):
            for j in range(len(board_matrix)):
                if (i, j) not in self.player.hit_history:
                    builder.button(
                        text=cell_mask[5],
                        callback_data=HitCellCallback(value=f'{i} {j}')
                    )
                else:
                    builder.button(
                        text=cell_mask[board_matrix[i][j]],
                        callback_data=HitCellCallback(value=f'{i} {j}')
                    )
                    
        return builder.as_markup()