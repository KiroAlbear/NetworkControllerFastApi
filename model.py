
from pydantic import BaseModel


class UserModel(BaseModel):
    id:int = 1
    firstName:str