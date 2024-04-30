from aiogram.types import (
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def next_prev_page(page_count):
    # Возвращает кнопки для пагинации и удаления записи из БД. Используется в Сохраненных
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='⬅Предыдущая', callback_data=f'prev_page')) if page_count != 1 else 0
    keyboard.add(InlineKeyboardButton(text='↩ Назад', callback_data=f'back_start'))
    keyboard.add(InlineKeyboardButton(text='Следующая➡', callback_data=f'next_page')) if page_count != 1 else 0
    keyboard.add(InlineKeyboardButton(text='Удалить❌', callback_data=f'delete_card'))
    return keyboard.adjust(3).as_markup()


async def save_info_card_or_back(is_record_in_db_or_id, type_info):
    # Функция сохранения или кнопки назад. Используется в информации о записи(боссе, NPC, оружии)
    callback_mapping = {
        'Weapons': 'back_weapon_list',
        'NPCs': 'back_npc_subtypes',
        'Bosses': 'back_bosses_game_mode'
    }
    keyboard = InlineKeyboardBuilder()
    callback_data = f'{callback_mapping[type_info]}'
    if not is_record_in_db_or_id:
        keyboard.add(InlineKeyboardButton(text='Сохранить✅', callback_data=f'save_card:{is_record_in_db_or_id}'))
    else:
        keyboard.add(
            InlineKeyboardButton(text='Удалить из избранного❌', callback_data=f'delete_card:{is_record_in_db_or_id}'))
    keyboard.add(InlineKeyboardButton(text='↩ Назад', callback_data=callback_data))
    return keyboard.adjust(1).as_markup()
