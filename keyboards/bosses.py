from aiogram.types import (
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from service.parser_bosses import get_boss_depending_on_game_mode


async def get_bosses_depending_game_mode(boss_game_mode):
    # Возвращает кнопки с именами боссов
    keyboard = InlineKeyboardBuilder()
    for boss_name in await get_boss_depending_on_game_mode(boss_game_mode):
        keyboard.add(InlineKeyboardButton(text=boss_name, callback_data=f'boss_info:{boss_name}'))
    keyboard.add(InlineKeyboardButton(text='↩ Назад', callback_data='back_bosses_btn'))
    return keyboard.adjust(1).as_markup()
