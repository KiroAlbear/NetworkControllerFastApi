from pydantic import BaseModel


from pydantic import BaseModel
class UserRechargeModel(BaseModel):
    id:int
    rechargeValue:int