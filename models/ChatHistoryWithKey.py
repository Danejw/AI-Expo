from typing import Dict, List
from models.ChatMessage import ChatMessage
from pydantic import BaseModel

class ChatHistoryWithKey(BaseModel):
    key: int
    history: List[ChatMessage]
    
    def to_dict(self) -> Dict[int, List[Dict]]:
        return {self.key: [message.dict() for message in self.history]}