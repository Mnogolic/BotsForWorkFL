from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestUser
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup


buttons = [
    [KeyboardButton('Добавить сервер')],
    [KeyboardButton('Добавить/Удалить администратора', request_user=KeyboardButtonRequestUser(0))]
]
main = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

buttons = [
    [KeyboardButton('Включен')],
    [KeyboardButton('Выключен')],
    [KeyboardButton('Назад')]
]
yes_or_no = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

#   Пока не использую 15.11.24
buttons = [
    [InlineKeyboardButton('Добавить', callback_data='send')],
    [InlineKeyboardButton('Отменить', callback_data='decline')]
]
confirm_server = InlineKeyboardMarkup(inline_keyboard=buttons)

buttons = [
    [KeyboardButton('Назад')]
]
back = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
