# in this security.py
# these function like hash password and create_jwt_token used to prevent user to access data without login
from passlib.context import CryptContext
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import jwt
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

pwd_context = CryptContext(schemes=["sha256_crypt", "des_crypt"], deprecated="auto")

def hash_password(password: str) -> str: # -> str hash_password will return data type in string 
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool: # -> bool verify_password will return data type in boolean
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt_token(data: dict, expires_delta_token: timedelta = None):
    to_encode = data.copy()

    # define time duration to expired token
    if expires_delta_token:
        expire = datetime.now(timezone.utc) + expires_delta_token
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)

    to_encode.update({"exp": expire})
    encode_jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt_token