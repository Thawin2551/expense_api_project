from schemas.user import User, UserUpdate
from security import hash_password, verify_password
from database import prisma

# Read all user function
async def read_all_user(): 
    users = await prisma.user.find_many()
    return users

# Get email function
async def get_user_by_email(email: str):
    user = await prisma.user.find_unique(
        where={"email": email}
    )
    return user

async def query_user(user_id: int):
    users = await prisma.user.find_unique(
        where={"id": user_id}
    )
    return users

async def create_user(user_data: User):
    # hashed password that get from api request post
    hashed_password = hash_password(user_data.password)

    # create a users object to create data
    users = await prisma.user.create(
        data = {
            "email": user_data.email,
            "password": hashed_password
        }
    )

    # send back data to user
    return users

async def edit_user(user_id: int, update_user: UserUpdate):
    updated_user = await prisma.user.update(
        # update user by query user_id as id in model User and use put function to update
        where = {"id": user_id},
        data = {
            "email": update_user.email,
            "password": hash_password(update_user.password)
        }
    )

    # return messages to told user that data had updated
    return updated_user

async def delete_user(user_id: int):
    deleted_user = await prisma.user.delete(
        where = {"id": user_id}
    )

    return deleted_user