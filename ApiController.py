import base64
import json
import math
import time

from typing import Dict, List
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from jwt import ExpiredSignatureError
from database.user_repository import UserRepository
from models.ChatHistoryWithKey import ChatHistoryWithKey
from models.UserModels import CreditAction, Token, User, UserInDB, UserRegistration, UserRegistrationResponse

from prompted_models.AlohaLani import AlohaLani
from prompted_models.CharacterDesigner import Character
from prompted_models.EnvironmentDesigner import Environment
from prompted_models.PaulGraham import PaulGraham
from prompted_models.PlotDesigner import Plot
from prompted_models.StoryDesigner import Story
from prompted_models.StyleDesigner import Style
from prompted_models.FunctionManager import FunctionManager
from prompted_models.Programmer import Programmer
from prompted_models.GrammarCorrection import GrammarCorrection
from prompted_models.Critic import Critic
from prompted_models.KeywordExtraction import KeyExtraction
from prompted_models.Summarizer import Summarization

from agents.AgentWithTools import AgentWithTools 

from models.ChatMessage import ChatMessage
from models.ChatHistory import ChatHistory

# Authentication
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status, Request
from datetime import timedelta
import auth


app = FastAPI()

# Exception handlers
@app.exception_handler(Exception)
def handle_exception(e: Exception):
    if isinstance(e, HTTPException):
        return {"error": str(e.detail)}
    else:
        return {"error": "An unexpected error occurred"}

@app.exception_handler(ExpiredSignatureError)
def handle_expired_signature_error(request: Request, exc: ExpiredSignatureError):
    return JSONResponse(status_code=401, content={"message": "Token has expired. Please login again."})





def get_user_repo() -> UserRepository:
    return UserRepository()

# bundles some logic to reduce repeating code
async def process_model_endpoint(model_instance, message, current_user) -> ChatMessage:    
    if check_user_credits(current_user): 
        message: ChatMessage = await model_instance.run_async(message.history)
        get_user_repo().remove_credits(current_user.username, math.ceil(message.cost))        
        return message
    else:        
        return ChatMessage(name="CoPilot", role="assistant", content="Oops, looks like you ran out of credits. You need more credits to make this call.", cost=0)


# check is the user has enough credits before going forward with the call to the endpoint
def check_user_credits(current_user: auth.User) -> bool:
    # Get the user's credits from the UserRepository
    user_repo = get_user_repo()
    user = user_repo.get_user(current_user.username)
    if user and user.credits >= 1:  # Adjust the credit threshold as needed
        return True
    return False




# Prompted Models
@app.post("/plot/")
async def PlotCreator(message: ChatHistory, current_user: auth.User = Depends(auth.get_current_active_user)) -> ChatMessage:
    return await process_model_endpoint(Plot(), message, current_user)

@app.post("/style/")
async def StyleCreator(message: ChatHistory, current_user: auth.User = Depends(auth.get_current_active_user)) -> ChatMessage:
    return await process_model_endpoint(Style(), message, current_user)

@app.post("/environment/")
async def EnvironmentCreator(message: ChatHistory, current_user: auth.User = Depends(auth.get_current_active_user)) -> ChatMessage:
    return await process_model_endpoint(Environment(), message, current_user)

@app.post("/character/")
async def CharacterCreator(message: ChatHistory, current_user: auth.User = Depends(auth.get_current_active_user)) -> ChatMessage:
    return await process_model_endpoint(Character(), message, current_user)

@app.post("/story/")
async def StoryCreator(message: ChatHistory, current_user: auth.User = Depends(auth.get_current_active_user)) -> ChatMessage:
    return await process_model_endpoint(Story(), message, current_user)

@app.post("/programmer/")
async def ProgramCreator(message: ChatHistory, current_user: auth.User = Depends(auth.get_current_active_user)) -> ChatMessage:
    return await process_model_endpoint(Programmer(), message, current_user)

@app.post("/grammar/")
async def GrammarCorrecter(message: ChatHistory, current_user: auth.User = Depends(auth.get_current_active_user)) -> ChatMessage:
    return await process_model_endpoint(GrammarCorrection(), message, current_user)

@app.post("/keywords/")
async def KeywordExtracter(message: ChatHistory, current_user: auth.User = Depends(auth.get_current_active_user)) -> ChatMessage:
    return await KeyExtraction(Environment(), message, current_user)

@app.post("/summarization/")
async def Summarizer(message: ChatHistory, current_user: auth.User = Depends(auth.get_current_active_user)) -> ChatMessage:
    return await process_model_endpoint(Summarization(), message, current_user)

@app.post("/critic/")
async def Criticizer(message: ChatHistory, current_user: auth.User = Depends(auth.get_current_active_user)) -> ChatMessage:
    return await process_model_endpoint(Critic(), message, current_user)

@app.post("/Aloha/")
async def Aloha(message: ChatHistory, current_user: auth.User = Depends(auth.get_current_active_user)) -> ChatMessage:
    return await process_model_endpoint(AlohaLani(), message, current_user)






# Authentication
@app.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):     
    user = get_user_repo().get_user(form_data.username)

    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type='bearer'
    )

@app.post("/register", response_model=UserRegistrationResponse)
async def register_user(user_data: UserRegistration):  
    user = get_user_repo().create_user(user_data)       
    access_token = auth.create_access_token(data={"sub": user.username})

    return UserRegistrationResponse (
        username=user.username,
        email=user.email,
        credits=user.credits,
        access_token=access_token,
        token_type='bearer'
    )


@app.get("/users/me/", response_model=User)
async def read_user_data(current_user: User = Depends(auth.get_current_user)):
    return current_user

@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(auth.get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]

@app.post("/users/me/credits/add/", response_model=User)
async def add_user_credits(credit_action: CreditAction, current_user: UserInDB = Depends(auth.get_current_active_user)): 
    user_repo = get_user_repo()
    user_repo.add_credits(current_user.username, credits=credit_action.credits)
    return user_repo.get_user(current_user.username)

@app.post("/users/me/credits/remove/", response_model=User)
async def remove_user_credits(credit_action: CreditAction, current_user: UserInDB = Depends(auth.get_current_active_user)):
    user_repo = get_user_repo()
    user_repo.remove_credits(current_user.username, credits=credit_action.credits)
    return user_repo.get_user(current_user.username)

@app.delete("/users/me/")
async def delete_current_user(current_user: UserInDB = Depends(auth.get_current_active_user)): 
    get_user_repo().delete_user(current_user.username)
    return {"message": "User deleted successfully"}


# manage chat histories
@app.get("/users/me/chat_histories/", response_model=List[ChatHistoryWithKey])
async def get_all_users_chat_histories(current_user: User = Depends(auth.get_current_active_user)):
    try:
        return get_user_repo().get_all_chat_histories(current_user.username)
    except Exception as e:
        return handle_exception(e)

# manage chat histories
@app.get("/users/me/chat_histories/", response_model=List[ChatHistoryWithKey])
async def get_all_users_chat_histories(current_user: User = Depends(auth.get_current_active_user)):
    return get_user_repo().get_all_chat_histories(current_user.username)

@app.get("/users/me/chat_history/{chat_history_id}/", response_model=ChatHistoryWithKey)
async def get_users_chat_history(chat_history_id: int, current_user: User = Depends(auth.get_current_active_user)):     
    return get_user_repo().get_chat_history_by_key(current_user.username, chat_history_id)

@app.post("/users/me/chat_histories/add/")
async def add_chat_history(chat_history: ChatHistoryWithKey, current_user: User = Depends(auth.get_current_active_user)): 
    get_user_repo().add_chat_history(current_user.username, chat_history)
    return {"message": "Chat history added successfully"}

@app.delete("/users/me/chat_histories/remove/{chat_history_id}/")
async def remove_chat_history(chat_history_id: int, current_user: User = Depends(auth.get_current_active_user)):   
    get_user_repo().remove_chat_history(current_user.username, chat_history_id)
    return {"message": "Chat history removed successfully"}





from fastapi.responses import RedirectResponse

@app.get("/authorize-streamlit")
async def authorize_streamlit(current_user: UserInDB = Depends(auth.get_current_active_user)):
    streamlit_app_url = f"http://localhost:8501/?token={current_user.token}"
    return RedirectResponse(url=streamlit_app_url, status_code=303)
