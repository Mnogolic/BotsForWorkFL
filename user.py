import keyboards
import texts
from pydantic import BaseModel

#   Навигация статусов
order_states = (
    'main',
    'input_server_name',
    'input_server_id',
    'input_server_password',
    'input_server_status',
    'confirm_server',
)
#   Перенаправление ответа
state_answers = {
    'main': {'text': 'Главное меню', 'reply_markup': keyboards.main},
    'input_server_name': {'text': 'Введите имя сервера:', 'reply_markup': keyboards.back},
    'input_server_id': {'text': 'Введите его ip:', 'reply_markup': keyboards.back},
    'input_server_password': {'text': 'Введите пароль:', 'reply_markup': keyboards.back},
    'input_server_status': {'text': 'Выберите состояние сервера: ', 'reply_markup': keyboards.yes_or_no},
}


class User:
    #   новая переменная, которая будет хранить имя сервера
    server_name = None
    server_id = None
    server_password = None
    amount = 0
    #   boolean переменная пусть будет по стандарту True
    server_status = None
    has_payed = True

    order_state_index = 0
    server_info = None
    tex2 = None

    #   ты что-то рассказывал про возникновение ошибок
    state_answers = state_answers
    order_states = order_states

    def __init__(self, id) -> None:
        self.id = id
        self.state_funcs = state_funcs

    async def get_order_state(self):
        return self.order_states[self.order_state_index]

    #   Переходм на следующую ступень state
    async def next_order_state(self, text=None, keyboard=None, photo=None, photos=None):
        self.order_state_index += 1
        return await self.state_prompt(text, keyboard, photo, photos)

    async def set_order_state(self, state_name: str):
        for i, state in enumerate(self.order_states):
            if state_name == state:
                self.order_state_index = i
                break

    async def state_prompt(self, text=None, keyboard=None, photo=None, photos=None, additional_data=None):
        state = await self.get_order_state()

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
            return answer

        return self.state_answers[state]

    async def dispatcher(self, data):
        state = await self.get_order_state()

        if data == 'Назад' and state != 'main':
            self.order_state_index -= 1
            return await self.state_prompt()
        elif data == 'Добавить сервер':
            return await self.next_order_state()
        else:
            try:
                return await self.state_funcs[state](self, data)
            except:
                return {'text': 'Некорректная команда №1. Если возникли проблемы - свяжитесь с @Zeportus'}

    #   Функция ставит имя серверу
    async def set_server_name(self, server_name):
        self.server_name = server_name
        return await self.next_order_state()

    #   Функция ставит id серверу
    async def set_server_id(self, server_id):
        self.server_id = server_id
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
            text2 = 'Проверьте введённые данные'

            text2 = texts.server_info.format(
                self.server_name,
                self.server_id,
                self.server_password,
                server_status
            )

            """
            splited_server_status = server_status.split()[0]
            text = (f'Проверьте данные сервера',
                    f'Заказ добавлен.',
                    f'\nИмя сервера:       {self.server_name}',
                    f'\nid сервера:           {self.server_id}',
                    f'\nПароль сеовера:  {self.server_password}',
                    f'\nСтатус сервера:    {splited_server_status}'
                    )
            text2 = ''.join(text)
            """
        #   Если пользователь выбрал кнопку 'выключен', записываем server_status = False
        elif server_status == 'выключен':
            self.server_status = False
            text2 = 'Проверьте введённые данные'
            """ 
            splited_server_status = server_status.split()[0]
            text = (f'Проверьте данные сервера',
                    f'Заказ добавлен.',
                    f'\nИмя сервера:       {self.server_name}',
                    f'\nid сервера:           {self.server_id}',
                    f'\nПароль сеовера:  {self.server_password}',
                    f'\nСтатус сервера:    {splited_server_status}'
                    )
            text2 = ''.join(text)
            """
            text2 = texts.server_info.format(
                self.server_name,
                self.server_id,
                self.server_password,
                server_status
            )
        else:
            text2 = 'Ошибка в выборе статуса'
        """
        await self.set_order_state('main')
        return {'text': text, 'reply_markup': keyboards.main}
        """
        return await self.next_order_state(text=text2, keyboard=keyboards.confirm_server)

    async def confirm_server(self, data):
        """
        if self.server_status:
            output_server_name = 'Включен'
        else:
            output_server_name = 'Выключен'
        """
        if data == 'send':
            text2 = 'Сервер добавлен.'
        else:
            text2 = 'Сервер не был добавлен.'
        await self.set_order_state('main')
        return {'text': text2, 'reply_markup': keyboards.main}


""" 
    async def confirm_server(self, data):
        if data == 'send':
            server_info = ServerInfo(
                server_name=self.server_name,
                server_id=self.server_id,
                server_password=self.server_password,
                server_status=self.server_status,
                has_payed=True
            )
            text = 'Сервер добавлен.'
        else:
            text = 'Сервер не был добавлен.'

        await self.set_order_state('main')
        return {'text': text, 'reply_markup': keyboards.main}
"""

state_funcs = {
    'input_server_name': User.set_server_name,
    'input_server_id': User.set_server_id,
    'input_server_password': User.set_server_password,
    'input_server_status': User.set_server_status,
    'confirm_server': User.confirm_server,
}
