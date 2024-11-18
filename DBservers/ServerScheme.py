from pydantic import BaseModel
import json
from typing import List


#   Класс из которого мы будем собирать базу данных в .json, основан на User из user.py
class ServerInfo(BaseModel):
    server_name: str
    server_ip: str
    server_password: str
    server_status: bool


# Модель для списка серверов
""" 
class ServerList(BaseModel):
    servers: List[ServerInfo]
"""


# Функция для добавления сервера в JSON файл с проверкой на дубликаты
def add_server(server_data: ServerInfo, filename="ServersDataBase.json"):
    # Загружаем текущие данные из JSON файла
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Проверяем, существует ли уже сервер с такими же данными (кроме имени)
    for server in data['servers']:
        # Сравниваем по server_id, server_password и server_status
        if server['server_ip'] == server_data.server_ip:
            print("Сервер с такими данными уже существует.\n")
            return  # Если сервер найден, выходим из функции и не добавляем нового

    # Если сервер с такими данными не найден, добавляем его в список
    data['servers'].append(server_data.dict())  # Добавляем сервер как словарь

    # Сохраняем обновленный список в JSON файл
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print("Сервер успешно добавлен.\n")


def display_servers(filename="ServersDataBase.json"):
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read().strip()

        if not content:
            print("Файл пуст.")
            return

        data = json.loads(content)
        if "servers" not in data or not data["servers"]:
            print("Нет данных о серверах.")
            return
        for server_dict in data["servers"]:
            server = ServerInfo(**server_dict)  # Создаем объект ServerInfo
            print(f"server_name: {server.server_name}")
            print(f"server_ip: {server.server_ip}")
            print(f"server_password: {server.server_password}")
            print(f"server_status: {server.server_status}")
            print("-" * 20)


def delete_server(server_name, filename="ServersDataBase.json"):
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read().strip()
        if not content:
            print("Файл пуст.")
            return
        data = json.loads(content)
        if "servers" not in data or not data["servers"]:
            print("Нет данных о серверах.")
            return

        server_found = False
        for server in data["servers"]:
            if server["server_name"] == server_name:
                data["servers"].remove(server)
                server_found = True
                print(f"Сервер с именем {server_name} удален.")
                break

        if not server_found:
            print(f"Сервер с именем {server_name} не найден.")
            return

        # Сохраняем обновленные данные в JSON файл
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


print('\n' * 2)
#   Передаём в бд сервер из тг
new_server = ServerInfo(
    server_name="Server1",
    server_ip="12345675765",
    server_password="password123",
    server_status=True
)
print('Пробуем добавить Server1')
add_server(new_server)
#   Покажи данные внутри .json
display_servers()
print('\n' * 4)

#   Передаём в бд сервер из тг
new_server = ServerInfo(
    server_name="Server2",
    server_ip="12345",
    server_password="password123",
    server_status=True
)
print('Пробуем добавить Server2')
add_server(new_server)
#   Покажи данные внутри .json
display_servers()
print('\n' * 4)

#   Передаём в бд сервер из тг
new_server = ServerInfo(
    server_name="Server3",
    server_ip="123455",
    server_password="password123",
    server_status=True
)
print('Пробуем добавить Server3')
add_server(new_server)
#   Покажи данные внутри .json
display_servers()


delete_server('Server3')
