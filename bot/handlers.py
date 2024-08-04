import math

from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
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
                    await msg.answer(text.no_content)
                else:
                    try:
                        response_data = await response.json()
                        messages = []
                        page = str(response_data.get('page', ''))
                        count_pages = str(math.ceil(response_data.get('total', '') / response_data.get('limit', '')))
                        if count_pages == '0':
                            count_pages = '1'
                        for message in response_data.get('messages', []):
                            author = message.get('author', '')
                            content = message.get('content', '')
                            messages.append(f"-{author}: {content}")
                        if count_pages == page:
                            await msg.answer("\n".join(messages) + "\n" + f"Страница {page} из {count_pages}")
                        else:
                            builder = InlineKeyboardBuilder()
                            builder.add(types.InlineKeyboardButton(
                                text=text.next_page,
                                callback_data=f'{str(int(page)+1)}'
                            ))
                            builder.adjust(1)
                            await msg.answer("\n".join(messages) + "\n" + f"Страница {page} из {count_pages}",
                                             reply_markup=builder.as_markup())
                    except Exception as e:
                        await msg.answer(e)
                        await msg.answer(text.error_text)
        else:
            payload = {
                "author": str(msg.from_user.id),
                "content": msg.text
            }
            async with session.post('http://46.229.214.108:80/api/v1/message/', json=payload,
                                    headers={'X-Client-IP': str(msg.from_user.id)}) as response:
                if response.status == 201:
                    await msg.answer(text.delivered)
                else:
                    await msg.answer(text.error_text)

@router.callback_query()
async def next_handler(callback: types.CallbackQuery):
    async with ClientSession() as session:
        async with session.get(f'http://46.229.214.108:80/api/v1/messages/', params={'page': int(callback.data)}) as response:
            try:
                response_data = await response.json()
                messages = []
                page = str(response_data.get('page', ''))
                count_pages = str(math.ceil(response_data.get('total', '') / response_data.get('limit', '')))
                if count_pages == '0':
                    count_pages = '1'
                for message in response_data.get('messages', []):
                    author = message.get('author', '')
                    content = message.get('content', '')
                    messages.append(f"-{author}: {content}")

                if count_pages == page:
                    await callback.bot.send_message(callback.from_user.id,
                                                    text="\n".join(messages) + "\n" + f"Страница {page} из {count_pages}")
                else:
                    builder = InlineKeyboardBuilder()
                    builder.add(types.InlineKeyboardButton(
                        text=text.next_page,
                        callback_data=f'{str(int(page) + 1)}'
                    ))
                    builder.adjust(1)
                    await callback.bot.send_message(callback.from_user.id,
                                                    text="\n".join(
                                                        messages) + "\n" + f"Страница {page} из {count_pages}",
                                                    reply_markup=builder.as_markup())
            except:
                await callback.bot.send_message(callback.from_user.id, text.error_text)