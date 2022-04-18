from pydantic import BaseModel


from pydantic import BaseModel
class UserLoginModel(BaseModel):
    email:str
    password:str