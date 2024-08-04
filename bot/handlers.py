from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiohttp import ClientSession

import kb
import text

router = Router()


@router.message(StateFilter(None), Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet, reply_markup=kb.main_menu)

@router.message(F.text)
async def handler(msg: Message):
    async with ClientSession() as session:
        if msg.text == text.get_mes:
            async with session.get('http://46.229.214.108:80/api/v1/messages/',) as response:
                if response.status == 204:
                    await msg.answer('Сообщений пока нет')
                else:
                    response_data = await response.json()
                    messages = []
                    for message in response_data:
                        author = message.get('author', '')
                        content = message.get('content', '')
                        messages.append(f"-{author}: {content}")
                    await msg.answer("\n".join(messages))
        else:
            payload = {
                "author": str(msg.from_user.id),
                "content": msg.text
            }
            async with session.post('http://46.229.214.108:80/api/v1/message/', json=payload,
                                    headers={'X-Client-IP': str(msg.from_user.id)}) as response:
                if response.status == 201:
                    await msg.answer('Сообщение успешно доставлено')
                else:
                    await msg.answer('Произошла непредвиденная ошибка, повторите ещё раз')