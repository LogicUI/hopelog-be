from pydantic import BaseModel
from typing import List, Dict


class ChatResponse(BaseModel):
    user_message: str
    conversation_history: List[Dict[str, str]]
