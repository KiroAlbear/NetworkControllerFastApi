from pydantic import BaseModel


class UserRechargeModel(BaseModel):
    id:str
    rechargeValue:int