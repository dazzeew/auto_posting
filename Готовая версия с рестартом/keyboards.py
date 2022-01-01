from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton

def main_keyboard():
    main_kb = ReplyKeyboardMarkup(resize_keyboard = True)
    btn3_1 = KeyboardButton("Создать пост")
    btn3_2 = KeyboardButton("Удалить пост")
    btn3_3 = KeyboardButton("Редактировать пост")
    btn3_4 = KeyboardButton("Список постов")
    main_kb.add(btn3_1,btn3_2).add(btn3_3,btn3_4)
    return main_kb

def create_keyboard():
    create_kb = ReplyKeyboardMarkup(resize_keyboard = True)
    btn1_1 = KeyboardButton("Отмена")
    create_kb.add(btn1_1)
    return create_kb


def post_data_keyboard():
    post_data = ReplyKeyboardMarkup(resize_keyboard = True)
    btn2_1 = KeyboardButton("Пост")
    btn2_2 = KeyboardButton("Дата")
    btn2_3 = KeyboardButton("Отмена")
    post_data.add(btn2_1,btn2_2).add(btn2_3)
    return post_data