from pydantic import BaseModel
import json
from pathlib2 import Path


class ServerInfo(BaseModel):
    name: str
    ip: str
    password: str
    status: bool


class ServerList(BaseModel):
    servers: list[ServerInfo]


class ServersManager:
    def __init__(self, path='servers_data_base.json'):
        self.path = Path(__file__).parent / path

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

    #   Без этой хитрости мы не сможем запросить данные из базы данных в user, в методе dispatcher()
    def get_from_bd(self):
        server_list = self._get_servers_list()
        return server_list

    def add_server(self, adding_server_info: ServerInfo):
        server_list = self._get_servers_list()

        for server_info in server_list.servers:
            if server_info.ip == adding_server_info.ip :
                print("Сервер с такими данными уже существует.\n")
                return

        server_list.servers.append(adding_server_info)

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(server_list.dict(), f, indent=4, ensure_ascii=False)
        print("Сервер успешно добавлен.\n")

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

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(server_list.dict(), f, indent=4, ensure_ascii=False)


""" 
# Тестирование
if __name__ == "__main__":
    path = "C:\\Users\\kasja\\PycharmProjects\\BotsForWorkFL\\servers_data_base.json"
    manager = ServersManager(path)

    print('\n' * 2)
    new_server = ServerInfo(
        name="Server1",
        ip="12345675765",
        password="password123",
        status=True
    )
    print('Пробуем добавить Server1')
    manager.add_server(new_server)
    manager.display_servers()
    print('\n' * 4)

    new_server = ServerInfo(
        name="Server2",
        ip="12345",
        password="password123",
        status=True
    )
    print('Пробуем добавить Server2')
    manager.add_server(new_server)
    manager.display_servers()
    print('\n' * 4)

    new_server = ServerInfo(
        name="Server3",
        ip="123455",
        password="password123",
        status=True
    )
    print('Пробуем добавить Server3')
    manager.add_server(new_server)
    manager.display_servers()

    print('\n' * 4)
    print('Удаляем сервер 3:')
    manager.delete_server('Server3')
    manager.display_servers()
"""
