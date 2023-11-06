from copy import deepcopy

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from database.database import jokes_db, MAX_PAGE_LEN
from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData, IsJokeData
from keyboards.bookmarks_kb import (create_jokes_keyboard,
                                    create_edit_keyboard)
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon import LEXICON
from services.file_handling import BOOK_PATH, load_jokes, rewrite_jokes
from config_data.config import Config, load_config
import os
import sys
import random
book: list
router = Router()
config: Config = load_config()

# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    book = load_jokes(os.path.join(sys.path[0],
                os.path.normpath(BOOK_PATH)))
    jokes_db['jokes'] = book
    await message.answer(LEXICON[message.text], )
    await message.answer(LEXICON['/jokes'],
                         reply_markup=create_jokes_keyboard(
                            jokes_db['jokes'],
                            jokes_db['page'],
                            jokes_db['max_page_len']
                         ))


@router.message(Command(commands='start@Shutnyarbl4Bot'))
async def process_start_command(message: Message):
    book = load_jokes(os.path.join(sys.path[0],
                os.path.normpath(BOOK_PATH)))
    jokes_db['jokes'] = book
    await message.answer(LEXICON[message.text], )
    await message.answer(LEXICON['/jokes'],
                         reply_markup=create_jokes_keyboard(
                            jokes_db['jokes'],
                            jokes_db['page'],
                            jokes_db['max_page_len']
                         ))

# Добавляет новую шутку в бд
@router.message(IsJokeData())
async def process_newjoke_command(message: Message):
    book = load_jokes(os.path.join(sys.path[0],
                os.path.normpath(BOOK_PATH)))
    book.append([message.text[1:-1]])
    jokes_db['jokes'] = book
    rewrite_jokes(os.path.join(sys.path[0],
                os.path.normpath(BOOK_PATH)), book)
    await message.answer(LEXICON['/jokes'],
                         reply_markup=create_jokes_keyboard(
                            jokes_db['jokes'],
                            jokes_db['page'],
                            jokes_db['max_page_len']
                         ))

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с шуткой
@router.callback_query(IsDigitCallbackData())
async def process_joke_press(callback: CallbackQuery):
    book = load_jokes(os.path.join(sys.path[0],
                os.path.normpath(BOOK_PATH)))
    jokes_db['jokes'] = book
    text = book[int(callback.data)][0]
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward'
        )
    )
    await callback.answer()


@router.callback_query(F.data == 'previous')
async def process_previous_press(callback: CallbackQuery):
    book = load_jokes(os.path.join(sys.path[0],
                os.path.normpath(BOOK_PATH)))
    jokes_db['jokes'] = book
    if jokes_db['page'] <= 1:
        await callback.answer()
    else:
        jokes_db['page'] -= 1
        await callback.message.edit_text(LEXICON['/jokes'],
                         reply_markup=create_jokes_keyboard(
                            jokes_db['jokes'],
                            jokes_db['page'],
                            jokes_db['max_page_len']
                         ))


@router.callback_query(F.data == 'next')
async def process_next_press(callback: CallbackQuery):
    book = load_jokes(os.path.join(sys.path[0],
                os.path.normpath(BOOK_PATH)))
    jokes_db['jokes'] = book
    if (jokes_db['page'] + 1) * jokes_db['max_page_len'] - len(jokes_db['jokes']) >= jokes_db['max_page_len']:
        await callback.answer()
    else:
        jokes_db['page'] += 1
        await callback.message.edit_text(LEXICON['/jokes'],
                         reply_markup=create_jokes_keyboard(
                            jokes_db['jokes'],
                            jokes_db['page'],
                            jokes_db['max_page_len']
                         ))



@router.callback_query(F.data == 'delprevious')
async def process_delprevious_press(callback: CallbackQuery):
    book = load_jokes(os.path.join(sys.path[0],
                os.path.normpath(BOOK_PATH)))
    jokes_db['jokes'] = book
    if jokes_db['page'] <= 1:
        await callback.answer()
    else:
        jokes_db['page'] -= 1
        await callback.message.edit_text(LEXICON['edit_jokes'],
                         reply_markup=create_edit_keyboard(
                            jokes_db['jokes'],
                            jokes_db['page'],
                            jokes_db['max_page_len']
                         ))



@router.callback_query(F.data == 'delnext')
async def process_delnext_press(callback: CallbackQuery):
    book = load_jokes(os.path.join(sys.path[0],
                os.path.normpath(BOOK_PATH)))
    jokes_db['jokes'] = book
    if (jokes_db['page'] + 1) * jokes_db['max_page_len'] - len(jokes_db['jokes']) >= jokes_db['max_page_len']:
        await callback.answer()
    else:
        jokes_db['page'] += 1
        await callback.message.edit_text(LEXICON['edit_jokes'],
                         reply_markup=create_edit_keyboard(
                            jokes_db['jokes'],
                            jokes_db['page'],
                            jokes_db['max_page_len']
                         ))

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперед"
# во время взаимодействия пользователя с сообщением-книгой
@router.callback_query(F.data == 'add')
async def process_add_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON["add_joke"],
        reply_markup=create_pagination_keyboard(
            'backward'
        )
    )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "назад"
# во время взаимодействия пользователя с сообщением-книгой
@router.callback_query(F.data == 'backward')
async def process_backward_press(callback: CallbackQuery):
    book = load_jokes(os.path.join(sys.path[0],
                os.path.normpath(BOOK_PATH)))
    jokes_db['jokes'] = book
    await callback.message.edit_text(LEXICON['/jokes'],
                                     reply_markup=create_jokes_keyboard(
                            jokes_db['jokes'],
                            jokes_db['page'],
                            jokes_db['max_page_len']
                         ))
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "редактировать" под списком закладок
@router.callback_query(F.data == 'edit_jokes')
async def process_edit_press(callback: CallbackQuery):
    if callback.from_user.id in config.tg_bot.admin_ids:
        book = load_jokes(os.path.join(sys.path[0],
                    os.path.normpath(BOOK_PATH)))
        jokes_db['jokes'] = book
        await callback.message.edit_text(
            text=LEXICON[callback.data],
            reply_markup=create_edit_keyboard(
                jokes_db['jokes'],
                jokes_db['page'],
                jokes_db['max_page_len']
            )
        )
    else:
        await callback.message.edit_text(
            text=LEXICON['no_permission'],
            reply_markup=create_pagination_keyboard(
            'backward'
            )
        )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок к удалению
@router.callback_query(IsDelBookmarkCallbackData())
async def process_del_bookmark_press(callback: CallbackQuery):
    book = load_jokes(os.path.join(sys.path[0],
        os.path.normpath(BOOK_PATH)))
    print(callback.data)
    book.pop(int(callback.data[:-3]))
    rewrite_jokes(os.path.join(sys.path[0],
        os.path.normpath(BOOK_PATH)), book)
    jokes_db['jokes'] = book
    if len(jokes_db['jokes']) > 0:
        await callback.message.edit_text(
            text=LEXICON['edit_jokes'],
            reply_markup=create_edit_keyboard(
                jokes_db['jokes'],
                jokes_db['page'],
                jokes_db['max_page_len']
            )
        )
    else:
        await callback.message.edit_text(text=LEXICON['no_jokes'],
                                         reply_markup=create_jokes_keyboard(
                                            jokes_db['jokes'],
                                            jokes_db['page'],
                                            jokes_db['max_page_len']
                                         ))
    await callback.answer()



# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "отменить" во время работы со списком закладок (просмотр и редактирование)
@router.callback_query(F.data == 'cancel')
async def process_cancel_press(callback: CallbackQuery):
    book = load_jokes(os.path.join(sys.path[0],
                os.path.normpath(BOOK_PATH)))
    jokes_db['jokes'] = book
    await callback.message.edit_text(LEXICON['/jokes'],
                        reply_markup=create_jokes_keyboard(
                            jokes_db['jokes'],
                            jokes_db['page'],
                            jokes_db['max_page_len']
                         ))
    await callback.answer()

@router.callback_query(F.data == 'random_joke')
async def process_random_joke_press(callback: CallbackQuery):
    book = load_jokes(os.path.join(sys.path[0],
                os.path.normpath(BOOK_PATH)))
    jokes_db['jokes'] = book
    text = book[int(random.randrange(0, len(book)))][0]
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward'
        )
    )
    await callback.answer()
