
from ast import walk
from fastapi import HTTPException
import email
from importlib.metadata import metadata
from select import select
from typing_extensions import Self
from unicodedata import name
import databases
from fastapi import Query
import sqlalchemy
from Models.loginModel import LoginModel

from Models.registerModel import RegisterModel
from Models.walletRechargeOrWithdrawModel import WalletRechargeOrWithdrawModel




class ProviderTable():
    __DATABASE_URL = "sqlite:///./users.db"
    __systemDatabase = databases.Database(__DATABASE_URL)
    __metaData = sqlalchemy.MetaData()
    tableName = "providers"

    id_ColumnName = "id"
    name_ColumnName = "name"
    email_ColumnName = "email"
    wallet_ColumnName = "wallet"
    phoneNumber_ColumnName = "phoneNumber"
    password_ColumnName = "password"
    __providerTable = 0

    def createAndReturnProviderTable(self):
        
        self.__providerTable = self.__getProviderTable()
       
        engine = sqlalchemy.create_engine(
        self.__DATABASE_URL,connect_args={"check_same_thread": False}
        )
        self.__metaData.create_all(engine)
        return self.__providerTable

    def __getProviderTable(self):
        providerTable = sqlalchemy.Table(
        self.tableName,
        self.__metaData,
        sqlalchemy.Column(self.id_ColumnName,sqlalchemy.Integer,primary_key = True),
        sqlalchemy.Column(self.name_ColumnName,sqlalchemy.String(500)),
        sqlalchemy.Column(self.email_ColumnName,sqlalchemy.String(500)),
        sqlalchemy.Column(self.wallet_ColumnName,sqlalchemy.Integer),
        sqlalchemy.Column(self.phoneNumber_ColumnName,sqlalchemy.String(500)),
        sqlalchemy.Column(self.password_ColumnName,sqlalchemy.String(500)))

        return providerTable

    async def loginProvider(self,loginModel:LoginModel):
        
        verification_query = "SELECT * FROM {} WHERE {}='{}' and {} = '{}'".format(
            self.tableName,

            self.email_ColumnName,
            loginModel.email,

            self.password_ColumnName,
            loginModel.password
        )

        record = await self.__systemDatabase.fetch_one(verification_query)
        if(record != None):
            return record
        else:
            raise HTTPException(
             status_code = 400,
             detail = "Wrong email or password"
            )
         

    async def insertNewProvider(self,registerModel:RegisterModel):

        query = self.__providerTable.insert().values(
        name = registerModel.name,
        email = registerModel.email,
        phoneNumber = registerModel.phoneNumber,
        password = registerModel.password,
        wallet = 0
    )
        ###################################################################################################

        phone_verification_query = "SELECT * FROM {} WHERE {}= '{}'".format(
           self.tableName,

           self.phoneNumber_ColumnName,
           registerModel.phoneNumber,
        )
        phone_verification_record = await self.__systemDatabase.fetch_all(phone_verification_query)

        ###################################################################################################

        email_verification_query = "SELECT * FROM {} WHERE {}= '{}' ".format(
           self.tableName,

           self.email_ColumnName,
           registerModel.email,
        )
        email_verification_record = await self.__systemDatabase.fetch_all(email_verification_query)

        ###################################################################################################
        
     
        if(len(phone_verification_record) > 0):
            raise HTTPException(
             status_code = 400,
             detail = "This Phone Number already exists"
            )
          
        elif(len(email_verification_record) > 0):
            raise HTTPException(
             status_code = 400,
             detail = "This Email already exists"
            )
        else:
           provider_id = await self.__systemDatabase.execute(query)
           return await self.getProviderData(provider_id)
    


    async def getProviderData(self,provider_id):

        query = "SELECT {},{},{},{},{} FROM {} WHERE {}={}".format(
        self.id_ColumnName,
        self.name_ColumnName,
        self.email_ColumnName,
        self.wallet_ColumnName,
        self.phoneNumber_ColumnName,

        self.tableName,

        self.id_ColumnName,
        
        provider_id)
        row = await self.__systemDatabase.fetch_one(query)
        return {
            self.id_ColumnName:row[0],
            self.name_ColumnName:row[1],
            self.email_ColumnName:row[2],
            self.wallet_ColumnName:row[3],
            self.phoneNumber_ColumnName:row[4],
        }



    async def addToWallet(self,providerWalletModel:WalletRechargeOrWithdrawModel):
        query = "UPDATE {} SET {} = {} + {} WHERE {} = {}".format(
            self.tableName,

            self.wallet_ColumnName,
            self.wallet_ColumnName,
            providerWalletModel.value,
            self.id_ColumnName,
            providerWalletModel.id
            )

        await self.__systemDatabase.execute(query)
        return await self.getProviderData(providerWalletModel.id)


    async def declineFromWallet(self,providerWalletModel:WalletRechargeOrWithdrawModel):
        query = "UPDATE {} SET {} = {} - {} WHERE {} = {} and {} > 0".format(
            self.tableName,

            self.wallet_ColumnName,
            self.wallet_ColumnName,
            providerWalletModel.value,

            self.id_ColumnName,
            providerWalletModel.id,
            self.wallet_ColumnName
            )

        success = await self.__systemDatabase.execute(query)
        if(success == 1):
            return await self.getProviderData(providerWalletModel.id)
        else:
            raise HTTPException(
             status_code = 400,
             detail = "Insufficient funds"
            )
