from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton


def create_keyboard():
    main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1_1 = KeyboardButton("Отмена")
    main_kb.add(btn1_1)
    return main_kb


def post_data_keyboard():
    post_data = ReplyKeyboardMarkup(resize_keyboard=True)
    btn2_1 = KeyboardButton("Пост")
    btn2_2 = KeyboardButton("Дата")
    btn2_3 = KeyboardButton("Отмена")
    post_data.add(btn2_1,btn2_2).add(btn2_3)
    return post_data