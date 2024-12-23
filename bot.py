from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from config import TOKEN_BOT
from handlers import weather
from aiogram.types import Message


# Инициализация бота и диспетчера
bot = Bot(TOKEN_BOT)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Регистрация хендлеров
@dp.message_handler(commands=["start"])
async def cmd_start(message: Message):
    await message.answer("Привет! Я Weather Bot. Я помогу узнать прогноз погоды. Введите /help, чтобы узнать, как я работаю.")

@dp.message_handler(commands=["help"])
async def cmd_help(message: Message):
    await message.answer("Доступные команды:\n"
                         "/start - Начать работу с ботом\n"
                         "/help - Информация о командах\n"
                         "/weather - Узнать прогноз погоды")

weather.register_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp)
