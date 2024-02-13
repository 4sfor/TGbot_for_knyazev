import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.dispatcher import router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from bot_create import dp
from aiogram.filters.command import Command
from data_base import sql_db
import bot_text


class FSMAdmin(StatesGroup):
    question = State()
    answer = State()
    admins = State()
    delete = State()



@dp.message(Command(bot_text.start_moderator.lower()))
async def start_command(message: types.Message, state: FSMContext):
    await state.set_state(FSMAdmin.admins)
    await message.answer(bot_text.start_admin)


@dp.message(FSMAdmin.admins)
async def start_admin(message: types.Message, state: FSMContext):
    if message.text in bot_text.key_world:
        context_date = str(message.from_user.id)
        await sql_db.sql_add_admin(context_date)
        await message.answer("доступ разрешен")


    else:
        await message.answer("ошибка в кодовом слове")

    await state.clear()


@dp.message(Command(bot_text.add_question_command.lower()))
async def add_question(message: types.Message, state: FSMContext):
    admins = await sql_db.is_admin()
    if str(message.from_user.id) in ((admin[0]) for admin in admins):
        await message.answer(bot_text.add_question)
        await state.set_state(FSMAdmin.question)
    else:
        print(str(message.from_user.id))
        print(admins)
        await message.answer("no")


@dp.message(FSMAdmin.question)
async def note_question(message: types.Message, state: FSMContext):
    await state.update_data(question=message.text)
    await message.answer(bot_text.add_answer)
    await state.set_state(FSMAdmin.answer)


@dp.message(FSMAdmin.answer)
async def add_answer(message: types.Message, state: FSMContext):
    count = await sql_db.count()
    data = await state.get_data()
    data["answer"] = message.text
    data["number"] = count + 1
    print(data)
    await sql_db.sql_add_question(data)
    await message.answer(bot_text.save_question)
    await state.clear()

@dp.message()
async def delete_question(message: types.Message, state: FSMContext):
    await message.answer(bot_text.delete_question)
    await state.update_data(number=message.text)
    await state.set_state(FSMAdmin.delete)


@dp.message(FSMAdmin.delete)
async def delete_question(message: types.Message):
    
    await sql_db.delete_question(message)



#юзер
@dp.message(Command(bot_text.start_user_command.lower()))
async def start(message: types.Message):
    await message.answer(bot_text.start_user)


@dp.message(Command(bot_text.get_question_command.lower()))
async def question(message: types.Message):
    await sql_db.sql_read_questions(message)
    await message.answer(bot_text.choose_question)

@dp.message()
async def choose_question(message: types.Message):
    await sql_db.sql_read_answer(message)