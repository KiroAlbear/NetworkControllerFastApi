
from ast import walk

import email
from importlib.metadata import metadata
from select import select
from unicodedata import name
import databases
from fastapi import Query
import sqlalchemy

from Models.userModel import UserModel
from Models.userRechargeModel import UserRechargeModel




class UserTable():
    __DATABASE_URL = "sqlite:///./users.db"
    _usersDatabase = databases.Database(__DATABASE_URL)
    __metaData = sqlalchemy.MetaData()
    tableName = "register"
    id_ColumnName = "id"
    name_ColumnName = "name"
    email_ColumnName = "email"
    wallet_ColumnName = "wallet"
    phoneNumber_ColumnName = "phoneNumber"
    password_ColumnName = "password"
    __register = 0

    def createAndReturnUserTable(self):
        
        register = self.__getRegisterTable()
        self.__register = register
        engine = sqlalchemy.create_engine(
        self.__DATABASE_URL,connect_args={"check_same_thread": False}
        )
        self.__metaData.create_all(engine)
        return register

    def __getRegisterTable(self):
        register = sqlalchemy.Table(
        self.tableName,
        self.__metaData,
        sqlalchemy.Column(self.id_ColumnName,sqlalchemy.Integer,primary_key = True),
        sqlalchemy.Column(self.name_ColumnName,sqlalchemy.String(500)),
        sqlalchemy.Column(self.email_ColumnName,sqlalchemy.String(500)),
        sqlalchemy.Column(self.wallet_ColumnName,sqlalchemy.Integer),
        sqlalchemy.Column(self.phoneNumber_ColumnName,sqlalchemy.String(500)),
        sqlalchemy.Column(self.password_ColumnName,sqlalchemy.String(500)))

        return register

    async def insertNewUser(self,userModel:UserModel):

        query = self.__register.insert().values(
        name = userModel.name,
        email = userModel.email,
        phoneNumber = userModel.phoneNumber,
        password = userModel.password,
        wallet = userModel.wallet
    )

    
        verification_query = "SELECT * FROM register WHERE {}={}".format(
            str(self.phoneNumber_ColumnName),

            str(userModel.phoneNumber),
        )
        record = await self._usersDatabase.fetch_all(verification_query)
     
        if(len(record) > 0):
            return {"Message":"This Phone Number already exists"}
        else:
           user_id = await self._usersDatabase.execute(query)
           return await self.getUserData(user_id)
    


    async def getUserData(self,userId):

        query = "SELECT {},{},{},{},{} FROM register WHERE id={}".format(
        self.id_ColumnName,
        self.name_ColumnName,
        self.email_ColumnName,
        self.wallet_ColumnName,
        self.phoneNumber_ColumnName,
        
        userId)
        row = await self._usersDatabase.fetch_one(query)
        return {
            self.id_ColumnName:row[0],
            self.name_ColumnName:row[1],
            self.email_ColumnName:row[2],
            self.wallet_ColumnName:row[3],
            self.phoneNumber_ColumnName:row[4],
        }



    async def rechargeWallet(self,userRechargeModel:UserRechargeModel):
        query = "UPDATE {} SET {} = {} + {} WHERE {} = {}".format(
            self.tableName,

            self.wallet_ColumnName,
            self.wallet_ColumnName,
            userRechargeModel.rechargeValue,
            self.id_ColumnName,
            userRechargeModel.id
            )

        await self._usersDatabase.execute(query)
        return await self.getUserData(userRechargeModel.id)
