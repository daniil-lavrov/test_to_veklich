import json
import logging

from fastapi import APIRouter, Request, Query
from aioredis import Redis
from starlette.responses import JSONResponse
from .models import Message, MessagesResponse
from .database import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
redis_client = Redis(host='redis', port=6379)

@router.get("/api/v1/messages/", response_model=MessagesResponse)
async def get_messages(page: int = Query(1, ge=1), limit: int = Query(10, le=100)):

    cached_messages = await redis_client.get('messages')
    skip = (page - 1) * limit

    if cached_messages:
        logger.info('Сообщения есть в кеше')
        messages = json.loads(cached_messages)
        total = len(messages)
        messages = messages[skip:skip + limit]
    else:
        logger.info('Сообщений нет в кеше')
        messages_to_cache = list(db.messages.find())
        total = len(messages_to_cache)
        messages = list(db.messages.find().skip(skip).limit(limit))
        for message in messages:
            if "_id" in message:
                del message["_id"]
        for message in messages_to_cache:
            if "_id" in message:
                del message["_id"]
        if messages_to_cache:
            await redis_client.set('messages', json.dumps(messages_to_cache))

    if not messages:
        return JSONResponse(status_code=204, content={"detail": "Сообщений пока нет"})

    return {
        'page': page,
        'limit': limit,
        'total': total,
        'messages': messages
    }

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
        await redis_client.delete('messages')
        logger.info('Кеш очищен')
        return JSONResponse(status_code=201, content={"detail": "Успешно добавлено"})
    except:
        return JSONResponse(status_code=500, content={"detail": "Повторите попытку позже"})
