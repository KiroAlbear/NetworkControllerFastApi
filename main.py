from atexit import register
import email
from importlib.metadata import metadata
from lib2to3.pytree import Base
import re
from unicodedata import name
from fastapi import Depends, FastAPI
from DataBaseTables.userTable import UserTable
from Models.userModel import UserModel
from Models.userRechargeModel import UserRechargeModel
import databases
import sqlalchemy



DATABASE_URL = "sqlite:///./users.db"
usersDatabase = databases.Database(DATABASE_URL)
userTable =  UserTable()
register = userTable.createAndReturnUserTable()

# metaData = sqlalchemy.MetaData()
# register = sqlalchemy.Table(
#     "register",
#     metaData,
#     sqlalchemy.Column("id",sqlalchemy.Integer,primary_key = True),
#     sqlalchemy.Column("name",sqlalchemy.String(500)),
#     sqlalchemy.Column("email",sqlalchemy.String(500)),
#     sqlalchemy.Column("wallet",sqlalchemy.Integer),
#     sqlalchemy.Column("phoneNumber",sqlalchemy.String(500)),
#     sqlalchemy.Column("password",sqlalchemy.String(500)),
# )
# engine = sqlalchemy.create_engine(
#     DATABASE_URL,connect_args={"check_same_thread": False}
# )
# metaData.create_all(engine)



app = FastAPI()

dp:list[UserModel] = []


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
async def addUser(r:UserModel):
    return await userTable.insertNewUser(r)

@app.post('/rechargeUserWallet')
async def addUser(r:UserRechargeModel):
    return await userTable.rechargeWallet(r)



