from pydantic import BaseModel


from pydantic import BaseModel
class EditProviderPackageModel(BaseModel):
    packageId:int
    newPrice:int
    newSizeMB:int