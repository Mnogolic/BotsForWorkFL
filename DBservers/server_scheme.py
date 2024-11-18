from pydantic import BaseModel
import json


class ServerInfo(BaseModel):
    name: str
    ip: str
    password: str
    status: bool


class ServerList(BaseModel):
    servers: list[ServerInfo]


# TODO: Создать отдельный класс (ServersManager) и перенести в него функции ниже
def add_server(adding_server_info: ServerInfo, filename="servers_data_base.json"):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
        server_list = ServerList(**data)

    for server_info in server_list.servers:
        if server_info.ip == adding_server_info.ip:
            print("Сервер с такими данными уже существует.\n")
            return

    server_list.servers.append(adding_server_info)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(server_list.dict(), f, indent=4, ensure_ascii=False)
    print("Сервер успешно добавлен.\n")


def display_servers(filename="servers_data_base.json"):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
        server_list = ServerList(**data)

    for server_info in server_list.servers:
        print(f"server_name: {server_info.name}")
        print(f"server_ip: {server_info.ip}")
        print(f"server_password: {server_info.password}")
        print(f"server_status: {server_info.status}")
        print("-" * 20)


def delete_server(server_name, filename="servers_data_base.json"):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
        server_list = ServerList(**data)

    server_info_to_delete = None
    for server_info in server_list.servers:
        if server_info.name == server_name:
            server_info_to_delete = server_info
            break

    if not server_info_to_delete:
        print(f"Сервер с именем {server_name} не найден.")
        return

    server_list.servers.remove(server_info_to_delete)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(server_list.dict(), f, indent=4, ensure_ascii=False)


# TODO: Шикарные тесты. Создать директорию tests, файл tests_server_manager.
#   Добавить эти тесты в виде функций, но сначала создать сам класс ServerManager
print('\n' * 2)
#   Передаём в бд сервер из тг
new_server = ServerInfo(
    name="Server1",
    ip="12345675765",
    password="password123",
    status=True
)
print('Пробуем добавить Server1')
add_server(new_server)
#   Покажи данные внутри .json
display_servers()
print('\n' * 4)

#   Передаём в бд сервер из тг
new_server = ServerInfo(
    name="Server2",
    ip="12345",
    password="password123",
    status=True
)
print('Пробуем добавить Server2')
add_server(new_server)
#   Покажи данные внутри .json
display_servers()
print('\n' * 4)

#   Передаём в бд сервер из тг
new_server = ServerInfo(
    name="Server3",
    ip="123455",
    password="password123",
    status=True
)
print('Пробуем добавить Server3')
add_server(new_server)
#   Покажи данные внутри .json
display_servers()


delete_server('Server3')
display_servers()
