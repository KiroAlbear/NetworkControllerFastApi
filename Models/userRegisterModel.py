
from pydantic import BaseModel



class UserRegisterModel(BaseModel):
    name:str
    email:str
    phoneNumber:str
    password:str
    wallet:int
