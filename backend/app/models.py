from typing import Optional, List

from pydantic import BaseModel


class Message(BaseModel):
    author: Optional[str] = None
    content: str

class MessagesResponse(BaseModel):
    page: int
    limit: int
    total: int
    messages: List[Message]
