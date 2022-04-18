
from pydantic import BaseModel


class RegisterModel(BaseModel):
    name:str
    email:str
    phoneNumber:str
    password:str
    wallet:int

