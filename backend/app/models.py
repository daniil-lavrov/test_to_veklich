from typing import Optional

from pydantic import BaseModel


class Message(BaseModel):
    author: Optional[int] = None
    content: str
