from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from service.parser_npc import get_npc_depending_on_type


async def npc_depending_on_types(type):
    # Возвращает всех NPC выбранного типа
    keyboard = InlineKeyboardBuilder()
    for content in await get_npc_depending_on_type(type):
        keyboard.add(InlineKeyboardButton(text=content.a['title'],
                                          callback_data=f'npc_depending_on_types:{content.a["title"]}'))
    keyboard.add(InlineKeyboardButton(text='↩ Назад', callback_data='back_npc_btn'))
    return keyboard.adjust(1).as_markup()
