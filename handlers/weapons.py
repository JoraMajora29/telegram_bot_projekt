from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bosses import save_info_card_or_back
from db_communicate import get_is_record_in_db
from keyboards.start import get_btns_types
from keyboards.weapon import (
    weapon_kinds_depending_on_type,
    weapon_game_mode_depending_on_kind,
    weapon_list_depending_on_game_mode
)
from service.parser_weapons import get_weapon_information

router = Router()


@router.callback_query(F.data == 'weapon_btn')
async def get_weapon_types(callback: CallbackQuery, state: FSMContext):
    # Функция получения типов оружия. Редактирует старое сообщение, если таковое есть, иначе
    # отправляет новое
    data = await state.get_data()
    message_id = data.get('message_id')
    if message_id:
        sent_message = await callback.message.edit_text('Типы оружия: ',
                                                        reply_markup=await get_btns_types('Weapon'))
        await state.update_data(message_id=sent_message.message_id)
    else:
        await callback.message.answer('Типы оружия: ',
                                      reply_markup=await get_btns_types('Weapon'))
    await callback.answer()


@router.callback_query(F.data.startswith('weapon_types'))
async def get_weapon_kinds(callback: CallbackQuery, state: FSMContext):
    # Функция получения видов оружия. Выводит их в зависимости от выбранного типа
    weapon_type = callback.data.split(':')[-1]
    await state.update_data(weapon_type=weapon_type)
    await callback.message.edit_text(f'Оружия типа: '
                                     f'\n{weapon_type}',
                                     reply_markup=await weapon_kinds_depending_on_type(weapon_type))


@router.callback_query(F.data.startswith('weapon_kind'))
async def get_weapon_game_mode(callback: CallbackQuery, state: FSMContext):
    # Функция получения игровых режимов оружия в зависимости от выбранного вида
    weapon_kind = callback.data.split(':')[-1]
    data = await state.get_data()
    weapon_type = data['weapon_type']
    await state.update_data(weapon_kind=weapon_kind)
    await callback.message.edit_text(f'Игровые режимы подтипа: '
                                     f'\n{weapon_kind}',
                                     reply_markup=await weapon_game_mode_depending_on_kind(
                                         [weapon_type, weapon_kind]
                                     ))
    await state.update_data(message_id=None)


@router.callback_query(F.data.startswith('weapon_list'))
async def get_weapon_list_depending_on_game_mode(callback: CallbackQuery, state: FSMContext):
    # Функция получения списка оружия в зависимости от игрового режима.
    # Удаляет сообщение информации об оружии, если оно было открыто, либо же возвращает список оружия
    weapon_game_mode = callback.data.split(':')[-1]
    data = await state.get_data()
    message_id = data.get('message_id')
    weapon_kind = data['weapon_kind']
    if message_id:
        await callback.bot.delete_message(callback.message.chat.id, message_id)
        await state.update_data(message_id=None)
    else:
        await callback.message.edit_text(f'Оружия подтипа: \n{weapon_kind}'
                                         f'\n\nИгрового режима: \n{weapon_game_mode}',
                                         reply_markup=await weapon_list_depending_on_game_mode(
                                             [weapon_kind, weapon_game_mode]
                                         ))


@router.callback_query(F.data.startswith('weapon_info'))
async def get_weapon_info(callback: CallbackQuery, state: FSMContext):
    # Выводит всю информацию о выбранном оружии. Есть возможность вернуться в оружие этого игрового режима или сохранить
    # информацию в БД. Либо удалить эту запись оттуда, если она уже там имеется.
    weapon_name = callback.data.split(':')[-1]
    info_weapon = await get_weapon_information(weapon_name)
    await callback.answer()

    image = info_weapon.pop('img')
    user_id = callback.from_user.id
    type_info = 'Weapons'
    is_weapon_in_db_or_id = await get_is_record_in_db(weapon_name, user_id, type_info)

    await state.update_data(main_info=info_weapon, image=image, type_info=type_info, favorite_id=is_weapon_in_db_or_id)
    message_text = "\n".join([f'{key}: {value}' for key, value in info_weapon.items()])
    await callback.message.answer_photo(image, caption=message_text,
                                        reply_markup=await save_info_card_or_back(is_weapon_in_db_or_id,
                                                                                  type_info))
