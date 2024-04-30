from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from db_communicate import get_is_record_in_db
from keyboards.bosses import (
    get_bosses_depending_game_mode,
)
from keyboards.favorites import save_info_card_or_back
from keyboards.start import get_btns_types
from service.parser_bosses import get_boss_information

router = Router()


@router.callback_query(F.data == 'bosses_btn')
async def get_bosses_types(callback: CallbackQuery, state: FSMContext):
    # Функция получения типов боссов. Редактирует старое сообщение, если таковое есть, иначе
    # отправляет новое
    data = await state.get_data()
    message_id = data.get('message_id')
    if message_id:
        await callback.message.edit_text('Типы боссов:',
                                         reply_markup=await get_btns_types('Bosses'))
        await state.update_data(message_id=None)
    else:
        await callback.message.answer('Типы боссов:',
                                      reply_markup=await get_btns_types('Bosses'))
    await callback.answer()


@router.callback_query(F.data.startswith('bosses_game_mode'))
async def get_bosses_game_mode(callback: CallbackQuery, state: FSMContext):
    # Функция получения игровых режимов боссов. Удаляет старое сообщение (информацию о боссе), или выводит всех
    # боссов определенного типа
    data = await state.get_data()
    message_id = data.get('message_id')
    boss_game_mode = callback.data.split(':')[-1]

    await state.update_data(boss_game_mode=boss_game_mode)
    if message_id:
        await callback.bot.delete_message(callback.message.chat.id, message_id)
    else:
        await callback.message.edit_text(f'Боссы типа:\n{boss_game_mode}',
                                         reply_markup=await get_bosses_depending_game_mode(boss_game_mode))


@router.callback_query(F.data.startswith('boss_info'))
async def get_boss_info(callback: CallbackQuery, state: FSMContext):
    # Выводит всю информацию о выбранном боссе. Есть возможность вернуться в боссов этого типа или сохранить
    # информацию в БД. Либо удалить эту запись оттуда, если она уже там имеется
    boss_name = callback.data.split(':')[-1]
    info_boss = await get_boss_information(boss_name)
    await callback.answer()

    image = info_boss.pop('img')
    user_id = callback.from_user.id
    type_info = 'Bosses'
    is_boss_in_db_or_id = await get_is_record_in_db(boss_name, user_id, type_info)

    await state.update_data(main_info=info_boss, image=image, type_info=type_info, favorite_id=is_boss_in_db_or_id)
    message_text = "\n".join([f'{key}: {value}' for key, value in info_boss.items()])
    await callback.message.answer_photo(image, caption=message_text,
                                        reply_markup=await save_info_card_or_back(is_boss_in_db_or_id,
                                                                                  type_info))
