
from ast import walk

import email
from importlib.metadata import metadata
from select import select
from typing_extensions import Self
from unicodedata import name
import databases
from fastapi import Query
import sqlalchemy
from Models.userLoginModel import UserLoginModel
from Models.userRegisterModel import UserRegisterModel
from Models.userRechargeModel import UserRechargeModel




class UserTable():
    __DATABASE_URL = "sqlite:///./users.db"
    _usersDatabase = databases.Database(__DATABASE_URL)
    __metaData = sqlalchemy.MetaData()
    tableName = "register"
    message_const = "Message"
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

    async def loginUser(self,userloginModel:UserLoginModel):
        
        verification_query = "SELECT * FROM register WHERE {}='{}' and {} = '{}'".format(

            self.email_ColumnName,
            userloginModel.email,

            self.password_ColumnName,
            userloginModel.password
        )

        record = await self._usersDatabase.fetch_one(verification_query)
        if(record != None):
            return record
        else:
           return {self.message_const:"Wrong email or password"}

    async def insertNewUser(self,userModel:UserRegisterModel):

        query = self.__register.insert().values(
        name = userModel.name,
        email = userModel.email,
        phoneNumber = userModel.phoneNumber,
        password = userModel.password,
        wallet = userModel.wallet
    )
        ###################################################################################################

        phone_verification_query = "SELECT * FROM register WHERE {}= '{}'".format(
           
           self.phoneNumber_ColumnName,
           userModel.phoneNumber,
        )
        phone_verification_record = await self._usersDatabase.fetch_all(phone_verification_query)

        ###################################################################################################

        email_verification_query = "SELECT * FROM register WHERE {}= '{}' ".format(
           
           self.email_ColumnName,
           userModel.email,
        )
        email_verification_record = await self._usersDatabase.fetch_all(email_verification_query)

        ###################################################################################################
        
     
        if(len(phone_verification_record) > 0):
            return {self.message_const:"This Phone Number already exists"}
        elif(len(email_verification_record) > 0):
            return {self.message_const:"This Email already exists"}
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


    async def payWithWallet(self,userRechargeModel:UserRechargeModel):
        query = "UPDATE {} SET {} = {} - {} WHERE {} = {} and {} > 0".format(
            self.tableName,

            self.wallet_ColumnName,
            self.wallet_ColumnName,
            userRechargeModel.rechargeValue,

            self.id_ColumnName,
            userRechargeModel.id,
            self.wallet_ColumnName
            )

        success = await self._usersDatabase.execute(query)
        if(success == 1):
            return await self.getUserData(userRechargeModel.id)
        else:
            return{self.message_const:"Insufficient funds"}
