from pydantic import BaseModel


class ServerInfo(BaseModel):
    name: str
    ip: str
    password: str
    status: bool


class ServerList(BaseModel):
    servers: list[ServerInfo]
