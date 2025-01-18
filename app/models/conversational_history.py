from pydantic import BaseModel
from typing import List


class ConversationEntry(BaseModel):
    user: str
    therapist: str


class ConversationalHistory(BaseModel):
    conversation_history: List[ConversationEntry]
