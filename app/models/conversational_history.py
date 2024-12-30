from pydantic import BaseModel
from typing import List, Dict

class ConversationalHistory(BaseModel):
    conversation_history: List[Dict[str, str]]
