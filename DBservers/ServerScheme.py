from pydantic import BaseModel
import json
from typing import List


#   Класс из которого мы будем собирать базу данных в .json, основан на User из user.py
# Класс для информации о сервере
class ServerInfo(BaseModel):
    server_name: str
    server_id: str
    server_password: str
    server_status: bool


# Модель для списка серверов
class ServerList(BaseModel):
    servers: List[ServerInfo]


# Функция для добавления сервера в JSON файл с проверкой на дубликаты
def add_server(server_data: dict, filename="servers.json"):
    try:
        # Загружаем текущие данные из JSON файла
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Создаем объект модели ServerInfo для нового сервера
        new_server = ServerInfo(**server_data)

        # Проверяем, существует ли уже сервер с такими же данными (кроме имени)
        for server in data['servers']:
            # Сравниваем по server_id, server_password и server_status
            if (server['server_id'] == new_server.server_id and
                    server['server_password'] == new_server.server_password):
                print("Сервер с такими данными уже существует.")
                return  # Если сервер найден, выходим из функции и не добавляем нового

        # Если сервер с такими данными не найден, добавляем его в список
        data['servers'].append(new_server.dict())  # Добавляем сервер как словарь

        # Сохраняем обновленный список в JSON файл
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print("Сервер успешно добавлен.")

    except FileNotFoundError:
        print("Файл с таким имененм не найден")


# Пример данных для нового сервера
new_server1 = {
    "server_name": "Server1",
    "server_id": "12345",
    "server_password": "password123",
    "server_status": True
}

new_server2 = {
    "server_name": "Server2",
    "server_id": "123456",
    "server_password": "password1234",
    "server_status": False
}

new_server3 = {
    "server_name": "Server3выаы",
    "server_id": "123456ываы",
    "server_password": "password1234выаыа",
    "server_status": False
}

# Добавление сервера в файл
print('Пробуем добавить уже ссществующий Srver1')
add_server(new_server1)
print('Пробуем добавить уже существующий Srver2')
add_server(new_server2)
print('Пробуем добавить ещё существующий Srver2')
add_server(new_server3)
