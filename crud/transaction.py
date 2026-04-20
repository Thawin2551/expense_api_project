from schemas.transaction import TransactionBase, TransactionCreate, TransactionUpdate, TransactionResponse, TransactionWithMessageResponse
from database import prisma
import calendar
from datetime import datetime

# Todo: Build transaction crud section like user and category crud section

# GET Transactions by month function
async def get_transaction_by_month(user_id: int, month: int = None, year: int = None):
    where_userId = {"userId": user_id}

    if month and year: # if month and year == True
        start_date = datetime(year, month, 1)

        _, last_day = calendar.monthrange(year, month)
        end_date = datetime(year, month, last_day, 23, 59, 59)

        where_userId["date"] = {
            "greater_than_equal": start_date,
            "less_than_equal": end_date
        }
    
        return await prisma.transaction.find_many(
            where=where_userId,
            include={"user": True, "category": True},
            order={"date": "desc"}
        )


# GET transaction summary
async def get_transaction_summary(user_id: int, month: int = None, year: int = None):
    where_userId = {"userId": user_id}

    # if month and year == True
    if month and year:
        start_date = datetime(year, month, 1)
        _, last_day = calendar.monthrange(year, month)
        end_date = datetime(year, month, last_day, 23, 59, 59)

        # query between start_date and end_date
        where_userId["date"] = {
            "greater_than_equal": start_date,
            "less_than_equal": end_date
        }   

        summary_data = await prisma.transaction.group_by(
            by=["type"],
            sum={"amount": True}, # sum all amount in that month and year
            where=where_userId,
        )

        # define income and expense start with 0
        total_income = 0
        total_expense = 0

        for item in summary_data:
            if item["type"] == "income":
                total_income = item.get("_sum", {}).get("amount", 0) or 0
            elif item["type"] == "expense":
                total_expense = item.get("_sum", {}).get("amount", 0) or 0
        
        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "net_balance": total_income - total_expense # income - expense we will get all money that remain
        }

# POST
async def create_transaction(transaction_create: TransactionCreate, user_id: int):
    new_transaction = await prisma.transaction.create(
        data = {
            "amount": transaction_create.amount,
            "type": transaction_create.type,
            "description": transaction_create.description,
            "categoryId": transaction_create.category_id,
            "userId": user_id,
        },
        include = {
            "category": True,
            "user": True 
        }   
    )

    return new_transaction
        
# GET
async def read_all_transaction(skip: int = 0, limit: int = 100):
    transactions = await prisma.transaction.find_many(
        skip=skip,
        take=limit,
        include={
            "category": True,
            "user": True
        },
        order={"date": "desc"}
    )   
    return transactions

# GET
async def query_transaction(transactionId: int):
    transaction = await prisma.transaction.find_unique(
        where={"id": transactionId},
        include={
            "category": True,
            "user": True
        }
    )
    return transaction

# PUT
async def edit_transaction(transactionId: int, transaction_update:TransactionUpdate, user_id: int, category_id: int):
    updated_transaction = await prisma.transaction.update(
        where={"id": transactionId},
        data = {
                "amount": transaction_update.amount,
                "type": transaction_update.type,
                "description": transaction_update.description,
                "categoryId": category_id,
                "userId" : user_id
            },
        include = {
            "category": True,
            "user": True
        }
    )

    return updated_transaction

# DELETE
async def delete_transaction(transactionId: int):
    deleted_transaction = await prisma.transaction.delete(
        where={"id": transactionId},
        include= {
            "category": True,
            "user": True
        }
    )
    return deleted_transaction
