from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

import kb
import text

router = Router()


@router.message(StateFilter(None), Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet, reply_markup=kb.main_menu)

@router.message(F.text)
async def handler(msg: Message):
    if msg.text == text.get_mes:
        await msg.answer('get')
    else:
        await msg.answer('zapisano')