from pydantic import BaseModel, EmailStr, ConfigDict
from schemas.user import UserResponse
from schemas.category import CategoryResponse

class TransactionBase(BaseModel):
    amount: float
    description: str
    type: str

class TransactionCreate(BaseModel):
    amount: float
    type: str
    description: str
    category_id: int

class TransactionUpdate(BaseModel):
    amount: float
    type:str
    description: str
    category_id: int

class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    description: str
    category: CategoryResponse
    user: UserResponse
    model_config = ConfigDict(from_attributes=True) # pydantic used to read object file through from_attribues=True

class TransactionWithMessageResponse(BaseModel):
    messages: str # Display string like a UserWithMessageResponse
    transaction: TransactionResponse
    model_config = ConfigDict(from_attributes=True)