from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestUser
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from all_keyboards.keyboard_generate_server_list import GenerateServersList

#   для генерации клавы
server_list_keyboard = GenerateServersList()

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
print('confirm_server', confirm_server)

#   Inline кнопка вывода серверов
buttons = server_list_keyboard.generate_buttons()
server_list = InlineKeyboardMarkup(inline_keyboard=buttons)
print('server_list', server_list)

buttons = [
    [KeyboardButton('Назад')]
]
back = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
