from atexit import register
import email
from importlib.metadata import metadata
from lib2to3.pytree import Base
import re
from unicodedata import name
from fastapi import Depends, FastAPI
from DataBaseTables.providerPackagesTable import ProviderPackagesTable
from DataBaseTables.userTable import UserTable
from DataBaseTables.providerTable import ProviderTable
from Models.deleteProviderPackageModel import DeleteProviderPackageModel
from Models.editProviderPackageModel import EditProviderPackageModel
from Models.getProviderPackageModel import GetProviderPackageModel
from Models.loginModel import LoginModel
from Models.addProviderPackageModel import AddProviderPackageModel
from Models.registerModel import RegisterModel

from Models.walletRechargeOrWithdrawModel import WalletRechargeOrWithdrawModel
import databases




DATABASE_URL = "sqlite:///./users.db"
usersDatabase = databases.Database(DATABASE_URL)

userTableFunctions =  UserTable()
providerTableFunctions =  ProviderTable()
providerPackagesTableFunctions =  ProviderPackagesTable()


userTableFunctions.createAndReturnUserTable()
providerTableFunctions.createAndReturnProviderTable()
providerPackagesTableFunctions.createAndReturnProviderTable()

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


@app.on_event("startup")
async def connect():
    await usersDatabase.connect()

@app.on_event("shutdown")
async def shutdown():
    await usersDatabase.disconnect()

## User APIS
######################################################################################

# @app.get("/Users")
# async def getAllUsers():
#     query =  register.select()
#     allUsers = await usersDatabase.fetch_all(query)
#     return allUsers


@app.post('/registerUser')
async def addUser(r:RegisterModel):
    return await userTableFunctions.insertNewUser(r)

@app.post('/loginUser')
async def loginUser(r:LoginModel):
    return await userTableFunctions.loginUser(r)

@app.post('/addToUserWallet')
async def rechargeUserWallet(r:WalletRechargeOrWithdrawModel):
    return await userTableFunctions.rechargeWallet(r)

@app.post('/withdrawFromUserWallet')
async def pay(r:WalletRechargeOrWithdrawModel):
    return await userTableFunctions.payWithWallet(r)

## Provider APIS
######################################################################################

@app.post('/registerProvider')
async def addUser(r:RegisterModel):
    return await providerTableFunctions.insertNewProvider(r)

@app.post('/loginProvider')
async def loginUser(r:LoginModel):
    return await providerTableFunctions.loginProvider(r)

@app.post('/addToProviderWallet')
async def rechargeUserWallet(r:WalletRechargeOrWithdrawModel):
    return await providerTableFunctions.addToWallet(r)

@app.post('/withdrawFromProviderWallet')
async def pay(r:WalletRechargeOrWithdrawModel):
    return await providerTableFunctions.declineFromWallet(r)


@app.post('/addProviderPackage')
async def addProviderPackage(r:AddProviderPackageModel):
    return await providerPackagesTableFunctions.insertPackage(r)

@app.get('/getProviderPackages/{provider_id}')
async def getProviderPackages(provider_id:int):
    return await providerPackagesTableFunctions.getProviderPackageData(provider_id)

@app.post('/updateProviderPackage')
async def updateProviderPackage(r:EditProviderPackageModel):
    return await providerPackagesTableFunctions.updatePackage(r)

@app.post('/deleteProviderPackage')
async def updateProviderPackage(r:DeleteProviderPackageModel):
    return await providerPackagesTableFunctions.deletePackage(r)


