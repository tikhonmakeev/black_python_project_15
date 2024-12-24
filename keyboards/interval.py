from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def interval_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        InlineKeyboardButton("1 день", callback_data="1"),
        InlineKeyboardButton("5 дней", callback_data="5"),
        InlineKeyboardButton("10 дней", callback_data="10")
    )
    return keyboard
