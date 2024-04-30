from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Кнопки для стартового сообщения
main_information_btns = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Weapons ⚔️', callback_data='weapon_btn')],
    [InlineKeyboardButton(text='Bosses 👿', callback_data='bosses_btn')],
    [InlineKeyboardButton(text='NPCs 🏠', callback_data='npc_btn')],
    [InlineKeyboardButton(text='Сохраненные 📘', callback_data='favorites_info')]
])

types_of_content = {
    'NPC': ['Town NPCs', 'Town pets', 'Town Slimes'],
    'Bosses': ['Pre-Hardmode bosses', 'Hardmode bosses', 'Event bosses'],
    'Weapon': {
        'Melee weapons': ['Swords', 'Yoyos', 'Spears', 'Boomerangs', 'Flails', 'Other'],
        'Ranged weapons': ['Bows and Repeaters', 'Guns', 'Launchers', 'Consumables', 'Grenades', 'Others'],
        'Magic weapons': ['Wands', 'Magic guns', 'Spell books', 'Others'],
        'Summoning weapons': ['Minion-summoning weapons', 'Sentry-summoning weapons', 'Whips'],
        'Other weapons': ['Placeable weapons', 'Explosives', 'Other weapons']
    }
}


async def get_btns_types(main_information):
    # Возвращает контент в зависимости от выбранного типа (боссы, NPC, оружия)
    keyboard = InlineKeyboardBuilder()
    for type in types_of_content[main_information]:
        if main_information == 'NPC':
            keyboard.add(InlineKeyboardButton(text=type, callback_data=f'npc_subtypes:{type}'))
        elif main_information == 'Bosses':
            keyboard.add(InlineKeyboardButton(text=type, callback_data=f'bosses_game_mode:{type}'))
        elif main_information == 'Weapon':
            keyboard.add(InlineKeyboardButton(text=type, callback_data=f'weapon_types:{type}'))
    keyboard.add(InlineKeyboardButton(text='↩ Назад', callback_data='back_start'))
    return keyboard.adjust(1).as_markup()
