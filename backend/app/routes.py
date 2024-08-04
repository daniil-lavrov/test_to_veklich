from fastapi import APIRouter, Request
from typing import List
from starlette.responses import JSONResponse
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
        return JSONResponse(status_code=204, content={"detail": "Сообщений пока нет"})

    return messages

@router.post("/api/v1/message/")
async def create_message(message: Message, request: Request):
    x_forwarded_for = request.headers.get('x-forwarded-for')
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(",")[0]
    else:
        client_ip = 'Anon'
    new_message = {
        "author": client_ip,
        "content": message.content
    }
    try:
        db.messages.insert_one(new_message)
        return JSONResponse(status_code=201, content={"detail": "Успешно добавлено"})
    except:
        return JSONResponse(status_code=500, content={"detail": "Повторите попытку позже"})
