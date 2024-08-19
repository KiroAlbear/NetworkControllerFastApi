import sqlalchemy
from DataBaseUtils.dataBaseCredintials import DataBaseCredentials
from Models.getConnectedUserModel import GetConnectedUserModel
from Models.registerConnectedUserToProviderModel import RegisterConnectedUserToProviderModel
from DataBaseUtils.dataBaseCommonFunction import DataBaseCommonFunctions
from Models.responseModels.responseObject import ResponseObject

class ProviderConnectedUsersTable():
    providerConnectedUsersTableName = "providerConnectedUsers"
    __providerConnectedUsersTable = 0
    __id_ColumnName = "id"
    __provider_uuid_ColumnName = "provider_uuid"
    __userMacAddress_ColumnName = "user_mac_address"

    __dataBaseCred = DataBaseCredentials()
    __dataBaseCommonFunctions = DataBaseCommonFunctions()


    async def deleteConnectedUsersTable(self):
       return await self.__dataBaseCommonFunctions.deleteTableFromDataBase(self.providerConnectedUsersTableName)

    def createAndReturnProviderConnectedUsersTable(self):
        self.__providerConnectedUsersTable = self.__dataBaseCommonFunctions.createTable(self.__createProviderConnectedUsersTable)
        # self.__providerConnectedUsersTable = self.__createProviderConnectedUsersTable()
       
        # engine = sqlalchemy.create_engine(
        # self.__dataBaseCred.DATABASE_URL,connect_args={"check_same_thread": False}
        # )
        # self.__dataBaseCred.metaData.create_all(engine)
        return self.__providerConnectedUsersTable
    

    
    def __createProviderConnectedUsersTable(self):
        providerUsersTable = sqlalchemy.Table(
        self.providerConnectedUsersTableName,
        self.__dataBaseCred.metaData,
        sqlalchemy.Column(self.__id_ColumnName,sqlalchemy.Integer,primary_key = True),
        sqlalchemy.Column(self.__userMacAddress_ColumnName,sqlalchemy.String(50),),
        sqlalchemy.Column(self.__provider_uuid_ColumnName,sqlalchemy.String(50),),)

        return providerUsersTable
    
    async def insertNewConnectedUserToProvider(self,registerModel:RegisterConnectedUserToProviderModel):
        try:
            query = self.__providerConnectedUsersTable.insert().values(
            provider_uuid = registerModel.provider_uuid,
            user_mac_address = registerModel.user_mac_address) 
            await self.__dataBaseCred.systemDatabase.execute(query)
            return ResponseObject(data=True,message="success",status=True)
        except:
            return ResponseObject(data=False,message="Error has occured",status=False)
         
        
    
    async def getConnectedUsersToSpecificProvider(self,getConnectedUserModel:GetConnectedUserModel):
         getConnectedUsersToProviderQuery = "SELECT * FROM {} WHERE {}= '{}'".format(
           self.providerConnectedUsersTableName,

           self.__provider_uuid_ColumnName,
           getConnectedUserModel.provider_uui,
        )
         return await self.__dataBaseCred.systemDatabase.execute(getConnectedUsersToProviderQuery)