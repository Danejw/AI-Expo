from typing import List
from models.ChatMessage import ChatMessage
from pydantic import BaseModel

class ChatHistory(BaseModel):
        history: List[ChatMessage]
