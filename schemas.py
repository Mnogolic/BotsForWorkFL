from pydantic import BaseModel


class ServerInfo(BaseModel):
    name: str
    id: str
    password: str
    status: bool
    has_payed: bool


