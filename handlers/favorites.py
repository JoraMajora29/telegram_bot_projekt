from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram.types import InputMediaPhoto

from handlers.bosses import save_info_card_or_back
from database.db_communicate import (
    get_info_by_user_id,
    add_favorite_to_db,
    delete_favorite_from_db
)
from keyboards.favorites import next_prev_page
from handlers.start import cmd_start

router = Router()


class Pagination(StatesGroup):
    page = State()


@router.callback_query(F.data.startswith('save_card'))
async def add_favorites_info(callback: CallbackQuery, state: FSMContext):
    # Функция добавляет запись в БД и меняет состояние кнопок с 'Сохранить' на 'Удалить из избранного'
    data = await state.get_data()

    user_id = callback.from_user.id
    data_info = data['main_info']
    type_info = data['type_info']
    data_info['img'] = data['image']

    favorite_id = await add_favorite_to_db(user_id, data_info, type_info)
    await callback.answer("Информация сохранена")
    await callback.message.edit_reply_markup(reply_markup=await save_info_card_or_back(favorite_id, type_info))


@router.callback_query(F.data.startswith('delete_card'))
async def delete_favorites_info(callback: CallbackQuery, state: FSMContext):
    # Функция удаляет запись из БД и меняет состояние кнопок с 'Удалить из избранного' на 'Сохранить', если запрос
    # пришел из информации о записи, либо же обновляет список сохраненных
    len_callback_data = len(callback.data.split(':'))
    data = await state.get_data()
    if len_callback_data != 1:
        favorite_id = callback.data.split(':')[-1]
    else:
        favorite_id = data['favorite_id']

    type_info = data['type_info']
    user_id = callback.from_user.id
    await delete_favorite_from_db(favorite_id, type_info)
    await callback.answer("Информация о боссе удалена")
    if len_callback_data == 1:
        await state.update_data(favorites=await get_info_by_user_id(user_id))
        await get_favorites_info(callback, state)
    else:
        await callback.message.edit_reply_markup(reply_markup=await save_info_card_or_back(False, type_info))


@router.callback_query(F.data.startswith('favorites_info'))
async def get_favorites_info(callback: CallbackQuery, state: FSMContext):
    # Возвращает информацию о избранной записи. Каждый раз выводит всего одну запись.
    # Можно листать избранные записи
    user_id = callback.from_user.id
    state_data = await state.get_data()

    if 'favorites' not in state_data:
        favorites = await get_info_by_user_id(user_id)
        if not favorites:
            await callback.answer("Нет сохраненных записей.")
            return
        await state.update_data(favorites=favorites)
        state_data = await state.get_data()

    favorites = state_data['favorites']
    page_count = len(favorites)
    if page_count != 0:
        current_page = state_data.get('page', 0) % page_count
        message_id = state_data.get('message_id')

        favorite = favorites[current_page]
        favorite_info = favorite[0]
        favorite_id = favorite[1]
        type_info = favorite[2]

        await callback.answer()
        await state.update_data(favorite_id=favorite_id, type_info=type_info)
        image = favorite_info.get('img')
        message_text = "\n".join([f'{key}: {value}' for key, value in favorite_info.items() if key != 'img'])

        if message_id:
            media = InputMediaPhoto(media=image, caption=message_text)
            await callback.bot.edit_message_media(chat_id=callback.from_user.id,
                                                  message_id=message_id,
                                                  media=media,
                                                  reply_markup=await next_prev_page(page_count))
        else:
            sent_message = await callback.message.answer_photo(image, caption=message_text,
                                                               reply_markup=await next_prev_page(page_count))
            await state.update_data(message_id=sent_message.message_id)
    else:
        await cmd_start(callback.message, state)
        return


@router.callback_query(F.data.startswith('prev_page'))
async def prev_page(callback: CallbackQuery, state: FSMContext):
    # Реализации пагинации. Информация о странице хранится в state
    current_page_data = await state.get_data()
    current_page = current_page_data.get('page', 0)
    current_page -= 1

    await state.update_data(page=current_page)
    await get_favorites_info(callback, state)


@router.callback_query(F.data.startswith('next_page'))
async def next_page(callback: CallbackQuery, state: FSMContext):
    # Реализации пагинации
    current_page_data = await state.get_data()
    current_page = current_page_data.get('page', 0)
    current_page += 1

    await state.update_data(page=current_page)
    await get_favorites_info(callback, state)
