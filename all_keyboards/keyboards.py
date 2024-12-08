from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestUser
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from all_keyboards.keyboard_generate_server_list import ButtonsGenerator

#   Кнопки main
buttons = [
    [KeyboardButton('Добавить сервер')],
    [KeyboardButton('Удалить сервер')],
    [KeyboardButton('Вывести все сервера')]
]
main = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

#   Кнопка, статуса сервера вкд/выкл
buttons = [
    [KeyboardButton('Включен')],
    [KeyboardButton('Выключен')],
    [KeyboardButton('Назад')]
]
yes_or_no = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

#   Кнопка, добавить ли сервер, данные которого ввёл пользователь
buttons = [
    [InlineKeyboardButton('Добавить', callback_data='send')],
    [InlineKeyboardButton('Отменить', callback_data='decline')]
]
confirm_server = InlineKeyboardMarkup(inline_keyboard=buttons)


#   Inline кнопка вывода серверов
def buttons_generator():
    server_list_keyboard_class = ButtonsGenerator()
    list_of_buttons = server_list_keyboard_class.generate_buttons()
    buttons = InlineKeyboardMarkup(inline_keyboard=list_of_buttons)
    return buttons


#   Кнопка, добавить ли сервер, данные которого ввёл пользователь
buttons = [
    [InlineKeyboardButton('Удалить', callback_data='удалить')],
    [InlineKeyboardButton('Отменить', callback_data='decline')]
]
delete_this_server = InlineKeyboardMarkup(inline_keyboard=buttons)

buttons = [
    [KeyboardButton('Назад')]
]
back = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
