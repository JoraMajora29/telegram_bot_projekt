from aiogram.types import (
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.start import types_of_content
from service.parser_weapons import (
    get_weapons_depending_on_type,
    weapons_types_and_subtypes
)


async def weapon_kinds_depending_on_type(type):
    # Возвращает виды оружия в зависимости от выбранного типа
    keyboard = InlineKeyboardBuilder()
    for kind_of_weapon in types_of_content['Weapon'][type]:
        keyboard.add(InlineKeyboardButton(text=kind_of_weapon,
                                          callback_data=f'weapon_kind:{kind_of_weapon}'))
    keyboard.add(InlineKeyboardButton(text='↩ Назад', callback_data='back_weapon_btn'))
    return keyboard.adjust(1).as_markup()


async def weapon_game_mode_depending_on_kind(type_and_kind):
    # Возвращает игровые режимы в зависимости от выбранного вида
    keyboard = InlineKeyboardBuilder()
    weapon_type = type_and_kind[0]
    weapon_kind = type_and_kind[-1]
    for game_mode in weapons_types_and_subtypes[weapon_type][weapon_kind]:
        keyboard.add(InlineKeyboardButton(text=game_mode,
                                          callback_data=f'weapon_list:{game_mode}'))
    keyboard.add(InlineKeyboardButton(text='↩ Назад',
                                      callback_data=f'back_weapon_types:{weapon_type}'))
    return keyboard.adjust(1).as_markup()


async def weapon_list_depending_on_game_mode(weapon_type_kind_and_mode):
    # Возвращает все оружия выбранного игрового режима
    keyboard = InlineKeyboardBuilder()
    weapon_kind = weapon_type_kind_and_mode[0]
    weapon_game_mode = weapon_type_kind_and_mode[1]
    for content in await get_weapons_depending_on_type([weapon_kind, weapon_game_mode]):
        keyboard.add(InlineKeyboardButton(text=content.a['title'],
                                          callback_data=f'weapon_info:{content.a["title"]}'))
    keyboard.add(InlineKeyboardButton(text='↩ Назад',
                                      callback_data=f'back_weapon_kind:{weapon_kind}'))
    return keyboard.adjust(1).as_markup()
