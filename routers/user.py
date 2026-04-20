from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import User, UserUpdate, UserResponse, UserWithMessageResponse, UserLogin
from crud import user as crud_user
from security import verify_password, hash_password, create_jwt_token
from typing import List # send back data as list type to user
from datetime import timedelta

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Login Function: Use to Verify and Save Data for user
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud_user.get_user_by_email(form_data.username)

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    access_token = create_jwt_token(
        data={"user_id": user.id},
        expires_delta_token=timedelta(minutes=60)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/", response_model=List[UserResponse])
async def read_all_user(): # limit select data from user, in case user not input limit, it will be 100
    users = await crud_user.read_all_user()
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def query_user(user_id: int):
        users = await crud_user.query_user(user_id=user_id)
        return users

@router.post("/", response_model=UserWithMessageResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
        new_user = await crud_user.create_user(user_data=user)
        return  {
            "messages": "User has been Created", 
            "user": new_user
        }       

@router.put("/{user_id}", response_model=UserWithMessageResponse)
async def edit_user(user_id: int, update_user: UserUpdate):
    updated_user = await crud_user.edit_user(user_id=user_id, update_user=update_user)
    return {
        "messages": f"user {user_id} has been updated",
        "user": updated_user
    }

@router.delete("/{user_id}", response_model=UserWithMessageResponse)
async def delete_user(user_id: int):
    deleted_user = await crud_user.delete_user(user_id=user_id)
    return {
        "messages": f"user {user_id} has been deleted",
        "user": deleted_user
    }