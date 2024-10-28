from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional


# Configuration for JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

# Pydantic models
class Token(BaseModel):
    access_token: str
    token_type: str
    
    
class TokenData(BaseModel):
    username: Optional[str] = None
    
    
class User(BaseModel):
    username: str
    
    
class UserInDB(User):
    hashed_password: str
    
    
# Fake database for users
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "hashed_password": pwd_context.hash("testpassword"),
        "auto_reply_enabled": True,
        "reply_delay_seconds": 5
    }
}

# Check if auto-reply is enabled for a user
def is_auto_reply_enabled(user):
    return user.get("auto_reply_enabled", False)

# Get reply delay from user settings
def get_reply_delay(user):
    return user.get("reply_delay_seconds", 5)

# Password hashing and verification functions
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Password hashing function
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Retrieve a user from the fake database
def get_user(db, username: str):
    user = db.get(username)
    if user:
        return UserInDB(**user)
    
# Authenticate user by username and password    
def authenticate_user(username: str, password: str):
    user = get_user(fake_users_db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


# JWT token creation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# JWT token verification
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = get_user(fake_users_db, token_data.username)
    if user is None:
        raise credentials_exception
    return user