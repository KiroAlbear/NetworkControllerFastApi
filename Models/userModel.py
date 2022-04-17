
from pydantic import BaseModel
from sqlalchemy import Integer



class UserModel(BaseModel):
    name:str
    email:str
    phoneNumber:str
    password:str
    wallet:int
