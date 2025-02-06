from pydantic import BaseModel


class EmailRequest(BaseModel):
    title: str
    message: str
