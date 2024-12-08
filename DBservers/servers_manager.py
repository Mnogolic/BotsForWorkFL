import json
from pathlib2 import Path
from DBservers.server_scheme import ServerInfo, ServerList


class ServersManager:
    def __init__(self, path='servers_data_base.json'):
        self.path = Path(__file__).parent / path

    # Нужен для проверки, и вывода через user, если сервер с таким ip уже существует

    def _get_servers_list(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)  # Попытка загрузки файла
                server_list = ServerList(**data)
        except json.JSONDecodeError:
            # Если файл пуст или содержит некорректный JSON
            print("База данных пуста или повреждена. Инициализируем пустой список.")
            server_list = ServerList(servers=[])
        except FileNotFoundError:
            # Если файл не найден
            print(f"Файл базы данных '{self.path}' не найден. Инициализируем пустой список.")
            server_list = ServerList(servers=[])

        return server_list

    def get_from_bd(self):
        server_list = self._get_servers_list()
        return server_list

    def add_server(self, adding_server_info: ServerInfo):
        server_list = self._get_servers_list()

        for server_info in server_list.servers:
            if server_info.ip == adding_server_info.ip:
                return "Сервер с таким ip уже существует, возвращаем вас в главное меню"

        server_list.servers.append(adding_server_info)

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(server_list.dict(), f, indent=4, ensure_ascii=False)
        print("Index: None, Сервер успешно добавлен.\n")
        return "Сервер успешно добавлен"

    def delete_server(self, server_name):
        server_list = self._get_servers_list()

        server_info_to_delete = None
        for server_info in server_list.servers:
            if server_info.name == server_name:
                server_info_to_delete = server_info
                break

        if not server_info_to_delete:
            print(f"Сервер с именем {server_name} не найден.")
            return

        server_list.servers.remove(server_info_to_delete)
        print("Index: None, Сервер успешно удалён.\n")
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(server_list.dict(), f, indent=4, ensure_ascii=False)
