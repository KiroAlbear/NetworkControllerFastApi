from pydantic import BaseModel


class ProviderPackageModel(BaseModel):
    providerId:int
    price:int
    sizeMB:int