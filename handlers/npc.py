from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bosses import save_info_card_or_back
from db_communicate import get_is_record_in_db
from keyboards.npc import npc_depending_on_types
from keyboards.start import get_btns_types
from service.parser_npc import get_npc_information

router = Router()


@router.callback_query(F.data == 'npc_btn')
async def get_npc_types(callback: CallbackQuery, state: FSMContext):
    # Функция получения типов NPC. Редактирует старое сообщение, если таковое есть, иначе
    # отправляет новое
    data = await state.get_data()
    message_id = data.get('message_id')
    if message_id:
        await callback.message.edit_text('Типы NPC',
                                         reply_markup=await get_btns_types('NPC'))
        await state.update_data(message_id=None)
    else:
        await callback.message.answer('Типы NPC',
                                      reply_markup=await get_btns_types('NPC'))
    await callback.answer()


@router.callback_query(F.data.startswith('npc_subtypes'))
async def get_npc_info(callback: CallbackQuery, state: FSMContext):
    # Функция получения NPC определенного типа. Удаляет старое сообщение (информацию о NPC), или выводит всех
    # NPC определенного типа
    npc_subtype = callback.data.split(':')[-1]
    data = await state.get_data()
    message_id = data.get('message_id')
    await state.update_data(npc_subtype=npc_subtype)
    if message_id:
        await callback.bot.delete_message(callback.message.chat.id, message_id)
        await state.update_data(message_id=None)
    else:
        await callback.message.edit_text(f'NPC типа:\n{npc_subtype}',
                                         reply_markup=await npc_depending_on_types(npc_subtype))


@router.callback_query(F.data.startswith('npc_depending_on_types'))
async def get_content_npc(callback: CallbackQuery, state: FSMContext):
    # Выводит всю информацию о выбранном NPC. Есть возможность вернуться в NPC этого типа или сохранить
    # информацию в БД. Либо удалить эту запись оттуда, если она уже там имеется
    npc_name = callback.data.split(':')[-1]
    info_npc = await get_npc_information(npc_name)
    await callback.answer()

    image = info_npc.pop('img')
    user_id = callback.from_user.id
    type_info = 'NPCs'

    is_npc_in_db_or_id = await get_is_record_in_db(npc_name, user_id, type_info)

    await state.update_data(main_info=info_npc, image=image, type_info=type_info, favorite_id=is_npc_in_db_or_id)
    message_text = "\n".join([f'{key}: {value}' for key, value in info_npc.items()])
    await callback.message.answer_photo(image, caption=message_text,
                                        reply_markup=await save_info_card_or_back(is_npc_in_db_or_id,
                                                                                  type_info))
