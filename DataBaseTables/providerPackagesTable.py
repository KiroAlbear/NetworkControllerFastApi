from http.client import HTTPException
import databases
import sqlalchemy
from DataBaseTables.providerTable import ProviderTable
from Models.providerPackageModel import ProviderPackageModel


class ProviderPackagesTable():
    __DATABASE_URL = "sqlite:///./users.db"
    __systemDatabase = databases.Database(__DATABASE_URL)
    __metaData = sqlalchemy.MetaData()
    tableName = "providersPackages"
    providerTableName = ProviderTable().tableName
    providerTableId_ColumnName = ProviderTable().id_ColumnName


    id_ColumnName = "id"
    myProviderTableId_ColumnName = "providerId"
    price_ColumnName = "price"
    size_ColumnName = "size"
    __providerPackagesTable = 0

    def createAndReturnProviderTable(self):
        
        self.__providerPackagesTable = self.__getProviderPackagesTable()
       
        engine = sqlalchemy.create_engine(
        self.__DATABASE_URL,connect_args={"check_same_thread": False}
        )
        self.__metaData.create_all(engine)
        return self.__providerPackagesTable



    def __getProviderPackagesTable(self):
        providerPackagesTable = sqlalchemy.Table(
        self.tableName,
        self.__metaData,
        sqlalchemy.Column(self.id_ColumnName,sqlalchemy.Integer,primary_key = True),
        sqlalchemy.Column(self.myProviderTableId_ColumnName,sqlalchemy.String(500)),
        sqlalchemy.Column(self.price_ColumnName,sqlalchemy.Integer),
        sqlalchemy.Column(self.size_ColumnName,sqlalchemy.Integer))

        return providerPackagesTable

    async def getProviderPackageData(self,provider_id):
        query = "SELECT {},{},{},{} FROM {} WHERE {}={}".format(
        self.id_ColumnName,
        self.myProviderTableId_ColumnName,
        self.price_ColumnName,
        self.size_ColumnName,

        self.tableName,

        self.myProviderTableId_ColumnName,
        provider_id)

        row = await self.__systemDatabase.fetch_one(query)
        return {
            self.id_ColumnName:row[0],
            self.myProviderTableId_ColumnName:row[1],
            self.price_ColumnName:row[2],
            self.size_ColumnName:row[3]
        }


    async def insertPackage(self,providerPackageModel:ProviderPackageModel):
        providerIdExistance_verification_query = "SELECT * FROM {} WHERE {}= '{}'".format(
           self.providerTableName,

           self.providerTableId_ColumnName,
           providerPackageModel.providerId,
        )
        provider_record = await self.__systemDatabase.fetch_all(providerIdExistance_verification_query)

        if(len(provider_record) == 0):
            raise HTTPException(
             status_code = 400,
             detail = "The provider is not exist"
            )
        else:
            insert_package_query = self.__providerPackagesTable.insert().values(
                providerPackageModel.providerId,
                providerPackageModel.price,
                providerPackageModel.sizeMB
            )
            package_id = await self.__systemDatabase.execute(insert_package_query)
            return await self.getProviderData(providerPackageModel.providerId)
