from aiogram import Router
from aiogram.types import Message


router = Router()


# Этот хендлер будет срабатывать на любые сообщения,
#  не предусмотренные логикой работы бота
@router.message()
async def send_echo(message: Message):
    await message.answer('Человек, я тебя не понимаю, используй '
                         'команды из меню.')
