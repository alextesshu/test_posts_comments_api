from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from pydantic import BaseModel
from app.auth import (
    authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, Token, get_current_user, fake_users_db, get_password_hash
)

router = APIRouter()

class RegisterUser(BaseModel):
    username: str
    password: str
    
    
class AutoReplyConfigUpdate(BaseModel):
    enabled: bool
    delay_seconds: int
    
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: RegisterUser):
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    hashed_password = get_password_hash(user.password)
    fake_users_db[user.username] = {
        "username": user.username,
        "hashed_password": hashed_password,
        "auto_reply_enabled": False,
        "reply_delay_seconds": 5
    }
    return {"message": "User registered successfully"}


@router.get("/")
async def read_users():
    return {"message": "Users endpoint is working!"}


@router.put("/update_auto_reply_config", status_code=status.HTTP_200_OK)
def update_auto_reply_config(config: AutoReplyConfigUpdate, current_user: str = Depends(get_current_user)):
    user = fake_users_db.get(current_user.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update auto-reply settings
    user["auto_reply_enabled"] = config.enabled
    user["reply_delay_seconds"] = config.delay_seconds

    return {"message": "Auto-reply configuration updated successfully"}