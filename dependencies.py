# This dependencies file has a get_current_user that used to verify that user through jwt token that get from security.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
import os
from database import prisma

oAuth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

async def get_current_user(token: str = Depends(oAuth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id: int = payload.get("user_id")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid Token. Please try again")
    except jwt.PyJWTError as e:
        # Debug Jwt Decode
        print(f"JWT Decode Error: {e}") 
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Couldn't validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await prisma.user.find_unique(
        where={"id": user_id}
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found in system. Please try again later"
        )

    return user