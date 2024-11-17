from pydantic import BaseModel
from user import User


#   Класс из которого мы будем собирать базу данных в .json, основан на User из user.py
class DBBase(BaseModel):
    server_name: str
    server_id: str
    server_password: str
    server_status: bool


