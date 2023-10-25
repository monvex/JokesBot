import os
import sys
import csv

BOOK_PATH = 'book/book.csv'


# Функция, формирующая словарь книги
def load_jokes(path: str) -> tuple:
    with open(file=path, mode='r', newline="", encoding='UTF8') as file:
        reader = csv.reader(file)
        book = []
        for row in reader:
            book.append([row[0]])
    return book



def rewrite_jokes(path: str, book: list) -> None:
    with open(file=path, mode='w', newline="", encoding='UTF8') as file:
        writer = csv.writer(file)
        for joke in book:
            joke = joke
        writer.writerows(book)


# Вызов функции prepare_book для подготовки книги из текстового файла
load_jokes(os.path.join(sys.path[0],
                os.path.normpath(BOOK_PATH)))
