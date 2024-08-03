from fastapi import APIRouter, HTTPException
from typing import List
from .models import Message
from .database import db

router = APIRouter()

@router.get("/api/v1/messages/", response_model=List[Message])
async def get_messages():
    messages = list(db.messages.find())
    for message in messages:
        if "_id" in message:
            del message["_id"]

    if not messages:
        raise HTTPException(status_code=204, detail="Сообщений пока нет")

    return messages

@router.post("/api/v1/message/")
async def create_message(message: Message):
    new_message = message.dict()
    db.messages.insert_one(new_message)
    return {
        "message": "Ваше сообщение успешно добавлено"
    }

