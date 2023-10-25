from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


def create_jokes_keyboard(args: list, page: int, maxlen: int) -> InlineKeyboardMarkup:
    # Создаем объект билдера
    builder = InlineKeyboardBuilder()
    startindex = (page-1) * maxlen
    # Заполняем клавиатуру кнопками-закладками в порядке возрастания
    if len(args) < startindex + maxlen:
        for i in range(startindex, len(args)):
            builder.row(InlineKeyboardButton(
                text=f'{i + 1} - {str(args[i][0][:50])}',
                callback_data=str(i)
            ))
    else:
        for i in range(startindex, startindex + maxlen):
            builder.row(InlineKeyboardButton(
                text=f'{i + 1} - {str(args[i][0][:50])}',
                callback_data=str(i)
            ))
    #
    builder.row(
        InlineKeyboardButton(
            text=LEXICON['previous'],
            callback_data='previous'
        ),
        InlineKeyboardButton(
            text=LEXICON['next'],
            callback_data='next'
        )
    )
    # Добавляем в клавиатуру две кнопки "Добавить" и "Отменить"
    builder.row(
        InlineKeyboardButton(
            text=LEXICON['edit_jokes_button'],
            callback_data='edit_jokes'
        ),
        InlineKeyboardButton(
            text=LEXICON['add'],
            callback_data='add'
        ),
        width=2
    )
    builder.row(
        InlineKeyboardButton(
            text=LEXICON['random_joke'],
            callback_data='random_joke'
        )
    )
    return builder.as_markup()


def create_edit_keyboard(args: list, page: int, maxlen: int) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    builder = InlineKeyboardBuilder()
    startindex = (page-1) * maxlen
    # Заполняем клавиатуру кнопками-закладками в порядке возрастания
    if len(args) < startindex + maxlen:
        for i in range(startindex, len(args)):
            builder.row(InlineKeyboardButton(
                text=f'{LEXICON["del"]} {i+1} - {args[i][0][:50]}',
                callback_data=f'{i}del'
            ))
    else:
        for i in range(startindex, startindex + maxlen):
            builder.row(InlineKeyboardButton(
                text=f'{LEXICON["del"]} {i+1} - {args[i][0][:50]}',
                callback_data=f'{i}del'
            ))
    builder.row(
        InlineKeyboardButton(
            text=LEXICON['previous'],
            callback_data='delprevious'
        ),
        InlineKeyboardButton(
            text=LEXICON['next'],
            callback_data='delnext'
        )
    )
    # Добавляем в конец клавиатуры кнопку "Отменить"
    builder.row(
        InlineKeyboardButton(
            text=LEXICON['backward'],
            callback_data='backward'
        )
    )
    return builder.as_markup()
