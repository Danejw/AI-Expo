from typing import Dict, List, Optional
from pydantic import BaseModel

from models.ChatHistory import ChatHistory


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    credits: int = 0
    chat_histories: Optional[Dict[int, ChatHistory]] = None

class UserInDB(User):
    hashed_password: str
    token :str = None
    
    
class CreditAction(BaseModel):
    credits: int
    
    
class UserRegistration(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] or None = None


class UserRegistrationResponse(BaseModel):
    username: str
    email: str
    full_name: str or None = None
    credits: int
    access_token: str
    token_type: str
 
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str or None = None
    
