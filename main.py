import asyncio
import logging

from aiogram import Bot, Dispatcher
from handlers import start, weapons, npc, back_btn, bosses, favorites

bot = Bot(token='6782021002:AAF86e5pXysVkeUMht4-UOguoalrcmQo0QU')
dp = Dispatcher()


# Функция регистрации всех router'ов, и запуск логирования для бота
async def main():
    dp.include_routers(
        start.router, weapons.router,
        npc.router, back_btn.router,
        bosses.router, favorites.router
    )
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)

# Запуск функции main в асинхронности
if __name__ == '__main__':
    asyncio.run(main())