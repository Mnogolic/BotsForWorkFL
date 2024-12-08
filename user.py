from all_keyboards import keyboards
import texts
from DBservers.servers_manager import ServersManager
from DBservers.server_scheme import ServerInfo

#   Навигация статусов
order_states = (
    'main',
    'input_server_name',
    'input_server_ip',
    'input_server_password',
    'input_server_status',
    'confirm_server',
    'choose_server_to_delete',
    'delete_this_one',
    'choose_server_to_off',
    'off_this_one',
    'choose_server_to_on',
    'on_this_one',
)
#   Перенаправление ответа 1
state_answers = {
    'main': {'text': 'Главное меню', 'reply_markup': keyboards.main},  # начало линий
    'input_server_name': {'text': 'Введите имя сервера:', 'reply_markup': keyboards.back},
    'input_server_ip': {'text': 'Введите его ip:', 'reply_markup': keyboards.back},
    'input_server_password': {'text': 'Введите пароль:', 'reply_markup': keyboards.back},
    'input_server_status': {'text': 'Выберите состояние сервера: ', 'reply_markup': keyboards.yes_or_no},
    'choose_server_to_delete': {'text': 'Выберите сервер для удаления', 'reply_markup': None},
    'delete_this_one': {'text': 'Вы уверены, что хотите удалить сервер?', 'reply_markup': keyboards.delete_this_server},
    'choose_server_to_off': {'text': 'Выберите сервер для выключения', 'reply_markup': None},
    'off_this_one': {'text': 'Вы уверены, что хотите выкулючить сервер?', 'reply_markup': keyboards.off_this_server},
    'choose_server_to_on': {'text': 'Выберите сервер для включения', 'reply_markup': None},
    'on_this_one': {'text': 'Вы уверены, что хотите включить сервер?', 'reply_markup': keyboards.on_this_server},
}


class User:
    #   функционал перемещения по state`ам
    order_state_index = 0
    state_answers = state_answers
    order_states = order_states

    #   новая переменная, которая будет хранить имя сервера
    server_name = None
    server_ip = None
    server_password = None
    server_status = None

    #   boolean переменная пусть будет по стандарту True
    #   amount = 0
    #   has_payed = True

    server_info = None

    #   обращение к калссу с функцциями в базе данных
    server_manager = ServersManager()

    def __init__(self, id) -> None:
        self.id = id
        self.state_funcs = state_funcs

    async def get_order_state(self):
        return self.order_states[self.order_state_index]

    #   Переходм на следующую ступень state
    async def next_order_state(self, text=None, keyboard=None, photo=None, photos=None):
        print('Index:', self.order_state_index)
        self.order_state_index += 1
        return await self.state_prompt(text, keyboard, photo, photos)

    async def set_order_state(self, state_name: str):
        for i, state in enumerate(self.order_states):
            if state_name == state:
                self.order_state_index = i
                break

    async def state_prompt(self, text=None, keyboard=None, photo=None, photos=None, additional_data=None):
        state = await self.get_order_state()
        print('Что в state -', state)
        if text or keyboard or photo or photos:
            answer = {}
            if text:
                answer['text'] = text
            if keyboard:
                answer['reply_markup'] = keyboard
            if photo:
                answer['photo'] = photo
            if photos:
                answer['photos'] = photos
            if additional_data:
                answer['additional_data'] = additional_data
            print('Что в answer -', answer, '\n\n')
            return answer

        return self.state_answers[state]

    async def dispatcher(self, data):
        state = await self.get_order_state()

        if data == 'Назад' and state != 'main':
            self.order_state_index -= 1
            return await self.state_prompt()

        elif data == 'Добавить сервер':  # Начало линия 1
            await self.set_order_state('input_server_name')
            print('Index 0')
            return await self.state_prompt()

        elif data == 'Вывести все сервера':
            print('Index None')
            return await self.show_all_servers()

        elif data == 'Удалить сервер':
            await self.set_order_state('choose_server_to_delete')
            print('Index 6')
            return await self.state_prompt(text=data, keyboard=keyboards.buttons_generator())

        elif data == 'Выключить сервер':
            await self.set_order_state('choose_server_to_off')
            return await self.state_prompt(text=data, keyboard=keyboards.buttons_true_generator())

        elif data == 'Включить сервер':
            await self.set_order_state('choose_server_to_on')
            return await self.state_prompt(text=data, keyboard=keyboards.buttons_false_generator())


        else:
            return await self.state_funcs[state](self, data)

        # else:
        # try:
        #    return await self.state_funcs[state](self, data)
        #except:
        #    return {'text': 'Некорректная команда №1. Если возникли проблемы - свяжитесь с @Zeportus'}

    #   Функция ставит имя серверу
    async def set_server_name(self, server_name):
        print(self.order_state_index)
        self.server_name = server_name
        return await self.next_order_state()

    #   Функция ставит id серверу
    async def set_server_ip(self, server_ip):
        self.server_ip = server_ip
        return await self.next_order_state()

    #   Фунция передающая пароль сервера
    async def set_server_password(self, server_password):
        self.server_password = server_password
        return await self.next_order_state()

    #   Функция должна ставить статус серверу True/False
    async def set_server_status(self, server_status):
        server_status = server_status.lower()
        #   Если пользователь выбрал кнопку 'включён', записываем server_status = True
        if server_status == 'включён' or server_status == 'включен':
            self.server_status = True

            text2 = texts.server_info.format(
                self.server_name,
                self.server_ip,
                self.server_password,
                server_status
            )

        #   Если пользователь выбрал кнопку 'выключен', записываем server_status = False
        elif server_status == 'выключен':
            self.server_status = False
            text2 = texts.server_info.format(
                self.server_name,
                self.server_ip,
                self.server_password,
                server_status
            )
        else:
            text2 = 'Ошибка в выборе статуса'

        return await self.next_order_state(text=text2, keyboard=keyboards.confirm_server)

    async def confirm_server(self, data):
        if data == 'send':
            new_server = ServerInfo(
                name=self.server_name,
                ip=self.server_ip,
                password=self.server_password,
                status=self.server_status
            )
            result = self.server_manager.add_server(new_server)  # Получаем результат добавления
            text2 = result  # Выводим результат ("Сервер с таким ip уже существует" или "Сервер успешно добавлен")
        else:
            text2 = 'Сервер не был добавлен.'

        # Возврат в главное меню
        await self.set_order_state('main')
        return {'text': text2, 'reply_markup': keyboards.main}

    #   Втоаря линия, удалние, если надо
    async def show_all_servers(self):
        # Получаем список серверов
        server_list = self.server_manager.get_from_bd()
        text2 = 'Сервера:\n\n'

        # Формируем текст для отображения серверов
        for server in server_list.servers:
            text2 += texts.server_info.format(
                server.name,
                server.ip,
                server.password,
                'включен' if server.status else 'выключен'
            )
            text2 += '\n'

        # Возвращаем сгенерированный текст
        return await self.state_prompt(text=text2, keyboard=keyboards.main)

    #   Пользовает выбирает сервер, который хочет удалить
    async def choose_server_to_delete(self, data):
        if data.lower() == 'decline':
            text2 = 'Главное меню'
            return await self.state_prompt(text=text2, keyboard=keyboards.main)
        else:
            self.server_name = data  # Сохраняем имя сервера
            text2 = f"Вы выбрали сервер '{self.server_name}' для удаления."
            return await self.next_order_state(text=text2, keyboard=keyboards.delete_this_server)

    #   Подтверждение у пользователя, точно ли он хочет его удалить
    async def delete_this_one(self, data):
        if data.lower() == 'удалить':
            if self.server_name:  # Проверка, что имя сервера установлено
                # Удаление сервера из базы
                self.server_manager.delete_server(self.server_name)
                text2 = f"Сервер '{self.server_name}' удалён."
            else:
                text2 = "Ошибка: Не выбран сервер для удаления."
        else:
            text2 = "Удаление отменено."

        # Возврат в главное меню
        await self.set_order_state('main')
        return {'text': text2, 'reply_markup': keyboards.main}

    # Пользователь выбирает сервер чтоб выключить
    async def choose_server_to_off(self, data):
        if data.lower() == 'decline':
            text2 = 'Главное меню'
            return await self.state_prompt(text=text2, keyboard=keyboards.main)
        else:
            self.server_name = data  # Сохраняем имя сервера
            text2 = f"Вы выбрали сервер '{self.server_name}' для выключения."
            return await self.next_order_state(text=text2, keyboard=keyboards.off_this_server)

    async def off_this_one(self, data):
        print('Функция вызвалаось, что в data -', data)
        if data.lower() == 'выключить':
            print('Записалось имя сервера при выключении?')
            if self.server_name:  # Проверка, что имя сервера установлено
                print('Да, записалось!')
                # выключение сервера в базе данных
                self.server_manager.off_server(server_name=self.server_name)
                text2 = f"Сервер '{self.server_name}' выключен."
            else:
                text2 = "Ошибка: Не выбран сервер для выключения."
        else:
            text2 = "Выключение отменено."

        # Возврат в главное меню
        await self.set_order_state('main')
        return {'text': text2, 'reply_markup': keyboards.main}

    # Пользователь выбирает сервер чтоб включить
    async def choose_server_to_on(self, data):
        if data.lower() == 'decline':
            text2 = 'Главное меню'
            return await self.state_prompt(text=text2, keyboard=keyboards.main)
        else:
            print('Сработает сохранение имени?')
            self.server_name = data  # Сохраняем имя сервера
            print('Сохранение имени сработало')
            text2 = f"Вы выбрали сервер '{self.server_name}' для включения."
            return await self.next_order_state(text=text2, keyboard=keyboards.on_this_server)

    async def on_this_one(self, data):
        if data.lower() == 'включить':
            if self.server_name:  # Проверка, что имя сервера установлено
                # включение сервера в базе данных
                print('Сработает ли server_manager.on_server')
                self.server_manager.on_server(server_name=self.server_name)
                print('Сработал server_manager.on_server')
                text2 = f"Сервер '{self.server_name}' включен."
            else:
                text2 = "Ошибка: Не выбран сервер для включения."
        else:
            text2 = "Включение отменено."

        # Возврат в главное меню
        await self.set_order_state('main')
        return {'text': text2, 'reply_markup': keyboards.main}


state_funcs = {
    'input_server_name': User.set_server_name,  # линия 1
    'input_server_ip': User.set_server_ip,  # линия 1
    'input_server_password': User.set_server_password,  # линия 1
    'input_server_status': User.set_server_status,  # линия 1
    'confirm_server': User.confirm_server,  # линия 1

    'choose_server_to_delete': User.choose_server_to_delete,  # линия 2
    'delete_this_one': User.delete_this_one,  # линия 2

    'choose_server_to_off': User.choose_server_to_off,  # линия 3
    'off_this_one': User.off_this_one,  # линия 3

    'choose_server_to_on': User.choose_server_to_on,  # линия 4
    'on_this_one': User.on_this_one,  # линия 4
}
