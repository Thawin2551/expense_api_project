from pydantic import BaseModel, EmailStr, ConfigDict

class Category(BaseModel):
    name: str
    icon: str

class CategoryUpdate(BaseModel):
    name: str
    icon: str

class CategoryResponse(BaseModel):
    id: int
    name: str
    icon: str 
    model_config = ConfigDict(from_attributes=True) # from_attributes=True is used for pydantic to read data though json object

class CategoryWithMessageResponse(BaseModel):
    messages: str
    category: CategoryResponse
    model_config = ConfigDict(from_attributes=True)