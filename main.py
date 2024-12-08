import json

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from all_keyboards import keyboards
from user import User

bot = Bot('7950408641:AAGSSORuNeTQDF5-YsJDrHztcPiqV-Cqlaw')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def get_user(id):
    data = await dp.storage.get_data(chat=id)

    if 'user' in data:
        return data, True
    else:
        with open('allow_users.json') as f:
            allow_users = json.load(f)['users']

        if str(id) not in allow_users:
            await bot.send_message(id, text='Доступ заблокирован.')
            return {}, False

        user = User(id)
        data = {'user': user, 'last_reply_markup': None}
        await dp.storage.set_data(chat=id, data=data)
        await bot.send_message(
            id,
            text='Сервер был перезапущен.',
            reply_markup=keyboards.main
        )
        # False - пользователь не был найден
        return data, False


async def save_user(id, data):
    await dp.storage.set_data(chat=id, data=data)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    with open('allow_users.json') as f:
        allow_users = json.load(f)['users']

    if str(message.from_id) not in allow_users:
        await message.answer(text='Доступ заблокирован.')
        return

    user = User(message.from_id)
    data = {'user': user, 'last_reply_markup': None}

    answer = await user.state_prompt()

    last_message = await message.answer(**answer)
    if last_message.reply_markup:
        data['last_reply_markup'] = last_message.message_id

    await save_user(user.id, data)


@dp.message_handler(content_types=types.ContentType.USER_SHARED)
async def answer_to_contact(message: types.Message):
    user_info = await get_user(message.from_id)
    # Если пользователь не был обнаружен, то тогда не обрабатываем его сообщение
    if not user_info[1]:
        return

    new_admin_id = str(message.user_shared.user_id)

    with open('allow_users.json') as f:
        allow_users = json.load(f)['users']

    if new_admin_id in allow_users:
        allow_users.remove(new_admin_id)
        await message.answer('Администратор УДАЛЕН')
    else:
        allow_users.append(new_admin_id)
        await message.answer('Администратор добавлен.\nЧтобы удалить - отправьте заново его контакт.')

    with open('allow_users.json', 'w') as f:
        data = {'users': allow_users}
        json.dump(data, f)


@dp.message_handler()
async def asnwer_to_prompt(message: types.Message):
    user_info = await get_user(message.from_id)
    # Если пользователь не был обнаружен, то тогда не обрабатываем его сообщение
    if not user_info[1]:
        return

    data = user_info[0]
    user = data['user']
    last_reply_markup = data['last_reply_markup']

    # Если у пользователя сохранено последнее сообщение с инлайн-клавиатурой, то удаляем эту клавиатуру
    if last_reply_markup:
        # try-except нужен, если пользователь удалит присланное ему сообщение с инлайн-клавиатурой и нажмет кнопку назад
        try:
            await bot.edit_message_reply_markup(user.id, last_reply_markup, reply_markup=None)
        except:
            pass

    answer = await user.dispatcher(message.text)

    last_message = await message.answer(**answer)

    if last_message.reply_markup:
        data['last_reply_markup'] = last_message.message_id

    await save_user(user.id, data)


@dp.callback_query_handler()
async def answer_to_callback(callback_query: types.CallbackQuery):
    user_info = await get_user(callback_query.from_user.id)
    # Если пользователь не был обнаружен, то тогда не обрабатываем его сообщение
    if not user_info[1]:
        return

    data = user_info[0]
    user = data['user']
    last_reply_markup = data['last_reply_markup']

    # Если у пользователя сохранено последнее сообщение с инлайн-клавиатурой, то удаляем эту клавиатуру
    if last_reply_markup:
        # try-except нужен, если пользователь удалит присланное ему сообщение с инлайн-клавиатурой и нажмет кнопку назад
        try:
            await bot.edit_message_reply_markup(user.id, last_reply_markup, reply_markup=None)
        except:
            pass

    answer = await user.dispatcher(callback_query.data)

    last_message = await bot.send_message(user.id, **answer)
    if last_message.reply_markup:
        data['last_reply_markup'] = last_message.message_id

    await save_user(user.id, data)


executor.start_polling(dp, skip_updates=True)
