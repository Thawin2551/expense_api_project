from fastapi import APIRouter, HTTPException, status, Depends
from crud import transaction as crud_transaction
from schemas.user import User
from schemas.transaction import TransactionBase, TransactionCreate, TransactionResponse, TransactionWithMessageResponse, TransactionUpdate, TransactionSummaryResponse
from dependencies import get_current_user
from typing import List, Optional # send back data as list type to user

router = APIRouter(
    prefix="/transaction",
    tags=["Transaction"]
)

# GET summary transaction this function must be on-top of all function to prevent error
@router.get("/summary", response_model=TransactionSummaryResponse)
async def get_transaction_summary(month: Optional[int] = None, year: Optional[int] = None, current_user: User = Depends(get_current_user)):
    summary = await crud_transaction.get_transaction_summary(
        user_id=current_user.id,
        month=month,
        year=year
    )

    return summary

# POST
# !!!! Next step we will  change format of url to use jwtToken instead user_id. That will help us to prevent user to access data without login
@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction_create: TransactionCreate, current_user: User = Depends(get_current_user)):
    new_transaction = await crud_transaction.create_transaction(
        transaction_create=transaction_create,
        user_id=current_user.id
        )
    return new_transaction

# GET
@router.get("/", response_model=List[TransactionResponse])
async def read_transaction(month: Optional[int] = None, year: Optional[int] = None, current_user: User = Depends(get_current_user)):
# if month = none it will skip condition month and year in transaction crud
    transactions = await crud_transaction.get_transaction_by_month(
        user_id=current_user.id,
        month=month,
        year=year
    )

    return transactions

# GET
@router.get("/{transactionId}", response_model=TransactionResponse)
async def query_transaction(transactionId: int):
    transaction = await crud_transaction.query_transaction(transactionId=transactionId)
    return transaction

# PUT
@router.put("/{transactionId}/user/{user_id}/category/{category_id}", response_model=TransactionWithMessageResponse)
async def edit_transaction(transactionId: int, user_id: int, category_id: int, transaction_update: TransactionUpdate):
    updated_transaction = await crud_transaction.edit_transaction(transactionId=transactionId, user_id=user_id, category_id=category_id, transaction_update=transaction_update)
    return {
        "messages": f"Transaction {transactionId} has been updated !",
        "transaction": updated_transaction
    }

# DELETE
@router.delete("/{transactionId}", response_model=TransactionWithMessageResponse)
async def delete_transaction(transactionId: int):
    deleted_transaction = await crud_transaction.delete_transaction(transactionId=transactionId)
    return {
        "messages": f"Transaction {transactionId} has been deleted !",
        "transaction": deleted_transaction
    }