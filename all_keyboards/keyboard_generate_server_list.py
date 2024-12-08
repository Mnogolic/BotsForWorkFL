from DBservers.servers_manager import ServersManager
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup


class ButtonsGenerator:
    #   обращение к калссу с функцциями в базе данных
    db = ServersManager()
    server_manager = ServersManager()

    """ 
    def give_me_server_list(self):
        server_list = self.db.get_from_bd()
        text2 = 'Список серверов:\n\n'

        # Добавляем только имена серверов
        for server in server_list.servers:
            text2 += f"{server.name}\n"

        print(text2)
    """

    def _give_me_server_list(self):
        server_list = self.db.get_from_bd()
        servers_names = []

        for server in server_list.servers:
            servers_names.append(server.name)

        return servers_names
        # Добавляем только имена серверов
        #   return [server.name for server in server_list.servers]

    def generate_buttons(self):
        servers_names = self._give_me_server_list()
        buttons = [
            [InlineKeyboardButton(server_name, callback_data=server_name)]
            for server_name in servers_names
        ]
        buttons.append([InlineKeyboardButton('Отменить', callback_data='decline')])

        return buttons


""" 
generator = GenerateServersList()
buttons_markup = generator.generate_buttons()
print(buttons_markup)
"""

#   server_names = generator.give_me_server_list()  # Получаем список серверов
#   buttons = generator.generate_buttons(server_names[0])  # Генерируем кнопки

#   print(buttons)
"""
generator = GenerateServersList()
print(generator.give_me_server_list())
"""
