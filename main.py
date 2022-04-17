import re
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from model import UserModel
import databases
import sqlalchemy

DATABASE_URL = "sqlite:///./users.db"
usersDatabase = databases.Database(DATABASE_URL)
metaData = sqlalchemy.MetaData()
register = sqlalchemy.Table(
    "register",
    metaData,
    sqlalchemy.Column("id",sqlalchemy.Integer,primary_key = True),
    sqlalchemy.Column("firstName",sqlalchemy.String(500))
)
engine = sqlalchemy.create_engine(
    DATABASE_URL,connect_args={"check_same_thread": False}
)
metaData.create_all(engine)



app = FastAPI()

dp:list[UserModel] = [
]


@app.on_event("startup")
async def connect():
    await usersDatabase.connect()

@app.on_event("shutdown")
async def shutdown():
    await usersDatabase.disconnect()


@app.get("/Users")
async def getAllUsers():
    query =  register.select()
    allUsers = await usersDatabase.fetch_all(query)
    return allUsers



@app.post('/addNewUser')
async def addUser(r:UserModel = Depends()):
    query = register.insert().values(
        firstName = r.firstName
    )
    record_id = await usersDatabase.execute(query)
    query = register.select().where(register.c.id == record_id)
    row = await usersDatabase.fetch_one(query)
    return {**row}

    # if(len(dp) == 0):
    #     dp.append(usermodel)


    # else:
    #     dp.append(UserModel(
    #         firstName=usermodel.firstName,
    #         lastname=usermodel.lastname,
    #         id=dp[dp.count-1].id + 1,
    #         phoneNumber=usermodel.phoneNumber,
    #         password=usermodel.password
    #         ))
    # return dp




