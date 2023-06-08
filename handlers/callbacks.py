from typing import Optional

from aiogram.filters.callback_data import CallbackData


class MyCellCallback(
    CallbackData,
    prefix = 'my'
):
    value: str
    
    
class HitCellCallback(
    CallbackData,
    prefix = 'hit'
):
    value: str
    
class ReadyCallback(
    CallbackData,
    prefix = 'ready'
):
    value: Optional[str]
    
class ExitCallback(
    CallbackData,
    prefix = 'exit'
):
    value: Optional[str]
    
    
class EndCallback(
    CallbackData,
    prefix = 'end'
):
    value: Optional[str]