from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.bosses import (
    get_bosses_game_mode,
    get_bosses_types
)
from handlers.npc import get_npc_info, get_npc_types
from handlers.start import cmd_start
from handlers.weapons import (
    get_weapon_list_depending_on_game_mode,
    get_weapon_game_mode,
    get_weapon_kinds,
    get_weapon_types
)

router = Router()


# Реализация кнопок назад для всего проекта. Логика одна - сохраняем message_id и вызываем предыдущую функцию
@router.callback_query(F.data == 'back_start')
async def back_to_start(callback: CallbackQuery, state: FSMContext):
    message_id = callback.message.message_id
    await state.update_data(message_id=message_id)
    await cmd_start(callback.message, state)


@router.callback_query(F.data.startswith('back_bosses_game_mode'))
async def back_to_bosses_game_mode(callback: CallbackQuery, state: FSMContext):
    message_id = callback.message.message_id
    await state.update_data(message_id=message_id)
    await get_bosses_game_mode(callback, state)


@router.callback_query(F.data == 'back_bosses_btn')
async def back_bosses_types(callback: CallbackQuery, state: FSMContext):
    message_id = callback.message.message_id
    await state.update_data(message_id=message_id)
    await get_bosses_types(callback, state)


@router.callback_query(F.data.startswith('back_weapon_list'))
async def back_to_weapon_list(callback: CallbackQuery, state: FSMContext):
    message_id = callback.message.message_id
    await state.update_data(message_id=message_id)
    await get_weapon_list_depending_on_game_mode(callback, state)


@router.callback_query(F.data.startswith('back_npc_subtypes'))
async def back_to_npc_subtypes(callback: CallbackQuery, state: FSMContext):
    message_id = callback.message.message_id
    await state.update_data(message_id=message_id)
    await get_npc_info(callback, state)


@router.callback_query(F.data.startswith('back_weapon_kind'))
async def back_to_weapon_kind(callback: CallbackQuery, state: FSMContext):
    message_id = callback.message.message_id
    await state.update_data(message_id=message_id)
    await get_weapon_game_mode(callback, state)


@router.callback_query(F.data.startswith('back_weapon_types'))
async def back_to_weapon_kind(callback: CallbackQuery, state: FSMContext):
    message_id = callback.message.message_id
    await state.update_data(message_id=message_id)
    await get_weapon_kinds(callback, state)


@router.callback_query(F.data.startswith('back_weapon_btn'))
async def back_to_weapon_btn(callback: CallbackQuery, state: FSMContext):
    message_id = callback.message.message_id
    await state.update_data(message_id=message_id)
    await get_weapon_types(callback, state)


@router.callback_query(F.data.startswith('back_npc_btn'))
async def back_to_npc_btn(callback: CallbackQuery, state: FSMContext):
    message_id = callback.message.message_id
    await state.update_data(message_id=message_id)
    await get_npc_types(callback, state)
