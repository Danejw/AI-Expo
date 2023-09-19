from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError
import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from database.user_repository import UserRepository
from models.UserModels import User, UserInDB, UserRegistration, UserRegistrationResponse, Token, TokenData

SECRET_KEY = "c9b7521ab7ff7fc87a0b34f5c5500ffe3fdeb7f923ed92470df62ab95c4eb960"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="login")


app = FastAPI()


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username:str):
    user_repo = UserRepository()
    user = user_repo.get_user(username)
    return user

def authenticate_user(username: str, password: str) -> UserInDB:
    user = get_user(username)
    
    if not user:
        return False
    
    if not verify_password(password, user.hashed_password):
        return False 
    
    return user
    
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

def get_user_by_token(token: str):
        # Verify and decode the token to get the username
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")           
            if username is None:
                raise HTTPException(status_code=400, detail="Token does not contain a valid subject")
        except JWTError:
            raise HTTPException(status_code=400, detail="Could not decode token")

        # Retrieve the user from the database using the username
        user = get_user(username)
        user.token = token
        return user

def get_current_user(token: str = Depends(oauth_2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    verify_token(token, credentials_exception)
    return get_user_by_token(token=token)


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return current_user

# Register a new user
def register_new_user(user_data: UserRegistration):
    user_repo = UserRepository()
    
    # Check if user already exists
    if user_data.username in db:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hash the password
    user_data.password = get_password_hash(user_data.password)

    # Create the new user using the user repository
    user_repo.create_user(user_data)

    # Create access token for the new user
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user_data.username}, expires_delta=access_token_expires)

    # Fetch the newly registered user data from the repository and convert it into UserInDB model
    registered_user = user_repo.get_user(user_data.username)

    # Construct the response
    response = UserRegistrationResponse(
        username=registered_user.username,
        email=registered_user.email,
        full_name=registered_user.full_name,
        credits=registered_user.credits,  # new users start with 0 credits
        access_token=access_token,
        token_type="bearer"
    )
    
    return response
