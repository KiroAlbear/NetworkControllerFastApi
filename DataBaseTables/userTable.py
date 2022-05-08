from fastapi import HTTPException
import databases
import sqlalchemy
from Models.loginModel import LoginModel
from Models.registerModel import RegisterModel
from Models.walletRechargeOrWithdrawModel import WalletRechargeOrWithdrawModel




class UserTable():
    __DATABASE_URL = "sqlite:///./users.db"
    __systemDatabase = databases.Database(__DATABASE_URL)
    __metaData = sqlalchemy.MetaData()
    tableName = "users"
    id_ColumnName = "id"
    name_ColumnName = "name"
    email_ColumnName = "email"
    wallet_ColumnName = "wallet"
    phoneNumber_ColumnName = "phoneNumber"
    password_ColumnName = "password"
    __usersTable = 0

    def createAndReturnUserTable(self):
        
        self.__usersTable = self.__getUsersTable()
    
        engine = sqlalchemy.create_engine(
        self.__DATABASE_URL,connect_args={"check_same_thread": False}
        )
        self.__metaData.create_all(engine)
        return self.__usersTable

    def __getUsersTable(self):
        usersTable = sqlalchemy.Table(
        self.tableName,
        self.__metaData,
        sqlalchemy.Column(self.id_ColumnName,sqlalchemy.Integer,primary_key = True),
        sqlalchemy.Column(self.name_ColumnName,sqlalchemy.String(500)),
        sqlalchemy.Column(self.email_ColumnName,sqlalchemy.String(500)),
        sqlalchemy.Column(self.wallet_ColumnName,sqlalchemy.Integer),
        sqlalchemy.Column(self.phoneNumber_ColumnName,sqlalchemy.String(500)),
        sqlalchemy.Column(self.password_ColumnName,sqlalchemy.String(500)))

        return usersTable

    async def loginUser(self,userloginModel:LoginModel):
        
        verification_query = "SELECT * FROM {} WHERE {}='{}' and {} = '{}'".format(

            self.tableName,

            self.email_ColumnName,
            userloginModel.email,

            self.password_ColumnName,
            userloginModel.password
        )

        record = await self.__systemDatabase.fetch_one(verification_query)
        if(record != None):
            return record
        else:
            raise HTTPException(
             status_code = 400,
             detail = "Wrong email or password"
            )

    async def insertNewUser(self,userModel:RegisterModel):

        query = self.__usersTable.insert().values(
        name = userModel.name,
        email = userModel.email,
        phoneNumber = userModel.phoneNumber,
        password = userModel.password,
        wallet = userModel.wallet
    )
        ###################################################################################################

        phone_verification_query = "SELECT * FROM {} WHERE {}= '{}'".format(
           self.tableName,

           self.phoneNumber_ColumnName,
           userModel.phoneNumber,
        )
        phone_verification_record = await self.__systemDatabase.fetch_all(phone_verification_query)

        ###################################################################################################

        email_verification_query = "SELECT * FROM {} WHERE {}= '{}' ".format(
           self.tableName,

           self.email_ColumnName,
           userModel.email,
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
           user_id = await self.__systemDatabase.execute(query)
           return await self.getUserData(user_id)
    


    async def getUserData(self,userId):

        query = "SELECT {},{},{},{},{} FROM {} WHERE {}={}".format(
        self.id_ColumnName,
        self.name_ColumnName,
        self.email_ColumnName,
        self.wallet_ColumnName,
        self.phoneNumber_ColumnName,

        self.id_ColumnName,

        self.tableName,
        
        userId)
        row = await self.__systemDatabase.fetch_one(query)
        return {
            self.id_ColumnName:row[0],
            self.name_ColumnName:row[1],
            self.email_ColumnName:row[2],
            self.wallet_ColumnName:row[3],
            self.phoneNumber_ColumnName:row[4],
        }



    async def rechargeWallet(self,walletRechargeOrWithdrawModel:WalletRechargeOrWithdrawModel):
        query = "UPDATE {} SET {} = {} + {} WHERE {} = {}".format(
            self.tableName,

            self.wallet_ColumnName,
            self.wallet_ColumnName,
            walletRechargeOrWithdrawModel.value,
            self.id_ColumnName,
            walletRechargeOrWithdrawModel.id
            )

        await self.__systemDatabase.execute(query)
        return await self.getUserData(walletRechargeOrWithdrawModel.id)


    async def payWithWallet(self,walletRechargeOrWithdrawModel:WalletRechargeOrWithdrawModel):
        query = "UPDATE {} SET {} = {} - {} WHERE {} = {} and {} > 0".format(
            self.tableName,

            self.wallet_ColumnName,
            self.wallet_ColumnName,
            walletRechargeOrWithdrawModel.value,

            self.id_ColumnName,
            walletRechargeOrWithdrawModel.id,
            self.wallet_ColumnName
            )

        success = await self.__systemDatabase.execute(query)
        if(success == 1):
            return await self.getUserData(walletRechargeOrWithdrawModel.id)
        else:
            raise HTTPException(
             status_code = 400,
             detail = "Insufficient funds"
            )
