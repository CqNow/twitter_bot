from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

menu__1222 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='/bot_start')
        ],
        [
            KeyboardButton(text='/bot_status'),
            KeyboardButton(text='/bot_stop')
        ]
    ],
    resize_keyboard=True
)