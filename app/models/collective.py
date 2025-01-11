from pydantic import BaseModel


class Collective(BaseModel):
    user_text: str
    emotion: str
    prompt: str
