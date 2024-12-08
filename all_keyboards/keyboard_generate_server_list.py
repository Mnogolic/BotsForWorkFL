from DBservers.servers_manager import ServersManager
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup


class ButtonsGenerator:
    #   обращение к калссу с функцциями в базе данных
    server_manager = ServersManager()

    def _give_me_server_list(self):
        server_list = self.server_manager.get_from_bd()
        servers_names = []

        for server in server_list.servers:
            servers_names.append(server.name)
        print('_give_me_server_list')
        return servers_names
        # Добавляем только имена серверов
        #   return [server.name for server in server_list.servers]

    def _give_me_server_list_true_status(self):
        server_list = self.server_manager.get_from_bd()
        servers_names = []

        for server in server_list.servers:
            if server.status:
                servers_names.append(server.name)
        return servers_names

    def _give_me_server_list_false_status(self):
        server_list = self.server_manager.get_from_bd()
        servers_names = []

        for server in server_list.servers:
            if not server.status:
                servers_names.append(server.name)
        return servers_names

    def generate_buttons(self, *args):

        servers_names = self._give_me_server_list()
        if not args:  # Если *args пустое
            servers_names = self._give_me_server_list()
        elif args[0] is True:  # Если передан True
            servers_names = self._give_me_server_list_true_status()
        elif args[0] is False:  # Если передан True
            servers_names = self._give_me_server_list_false_status()
        else:
            raise ValueError("Некорректный аргумент для generate_buttons.")

        buttons = [
            [InlineKeyboardButton(server_name, callback_data=server_name)]
            for server_name in servers_names
        ]
        buttons.append([InlineKeyboardButton('Отменить', callback_data='decline')])

        return buttons

""" 
buttons = ButtonsGenerator()
buttons0 = buttons.generate_buttons()
buttons_true = buttons.generate_buttons(False)
buttons_false = buttons.generate_buttons(True)
print("generate_buttons -", buttons0)
print("generate_buttons(False) -", buttons_true)
print("generate_buttons(True) -", buttons_false)
"""
