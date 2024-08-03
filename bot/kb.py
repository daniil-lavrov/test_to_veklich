from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import text


main_menu = [
    [KeyboardButton(text=text.get_mes)]
]
main_menu = ReplyKeyboardMarkup(keyboard=main_menu, resize_keyboard=True)