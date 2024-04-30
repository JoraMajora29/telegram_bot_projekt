from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.start import main_information_btns

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    # Функция запуска бота, реагирует на /start. Удаляет прошлое сообщение, либо выводит новое
    data = await state.get_data()
    message_id = data.get('message_id')
    await state.clear()
    if message_id:
        await message.bot.delete_message(message.chat.id, message_id)
    else:
        await message.answer('Бот работает! \n\nВыберите тип контента:',
                             reply_markup=main_information_btns)
