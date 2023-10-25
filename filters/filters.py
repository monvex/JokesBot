from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message


# Фильтр, проверяющий то, что callback_data состоит из цифр
class IsDigitCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.isdigit()


class IsDelBookmarkCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.endswith('del') and callback.data[:-3].isdigit()


class IsJokeData(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text.startswith('"') and message.text.endswith('"')
