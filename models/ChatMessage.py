
from pydantic import BaseModel
from typing import Optional

class ChatMessage(BaseModel):
        name: str
        role: str
        content: str
        cost: Optional[float]=None
        
        def __str__(self):
            return f"{self.role}: {self.name} - {self.content} - {self.cost}"
