from aiogram import Router, types, F
from aiogram.filters import or_f
from aiogram.filters.command import Command
from aiogram.utils.formatting import as_marked_section, Bold, as_list
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_querry import orm_get_products
from filters.chat_tipes import ChatTypeFilter
from keyboards import reply
from keyboards.reply import get_keyboard

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


@user_private_router.message(or_f(Command('start'), F.text.lower().contains('старт')))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет, я виртуальный помощник",
        reply_markup=get_keyboard(
            "Меню",
            "О магазине",
            "Варианты оплаты",
            "Варианты доставки",
            placeholder="Что вас интересует?",
            sizes=(2, 2)
        ),
    )


@user_private_router.message(or_f(Command('menu'), F.text.lower().contains('меню')))
async def get_admins(message: types.Message, session:  AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f"<strong>{product.name}\
                    </strong>\n{product.description}\nСтоимость: {round(product.price, 2)}",
        )
    await message.answer("Вот меню:")


@user_private_router.message(or_f(Command('about'), F.text.lower().contains('о магазине')))
async def menu_about(message: types.Message):
    await message.reply("О нас:", reply_markup=reply.get_keyboard())


@user_private_router.message(or_f(Command('payment'), F.text.lower().contains('варианты оплаты')))
async def menu_payment(message: types.Message):
    text = as_marked_section(
        Bold("Варианты оплаты:"),
        "Картой в боте",
        "При получении карта/кеш",
        "В заведении",
        marker='✅ '
    )
    await message.answer(text.as_html())


@user_private_router.message(or_f(Command('delivery'), F.text.lower().contains('доставк')))
async def menu_delivery(message: types.Message):
    text = as_list(
        as_marked_section(
            Bold("Варианты доставки/заказа:"),
            "Курьер",
            "Самовынос (сейчас прибегу заберу)",
            "Покушаю у Вас (сейчас прибегу)",
            marker='✅ '
        ),
        as_marked_section(
            Bold("Нельзя:"),
            "Почта",
            "Голуби",
            marker='❌ '
        ),
        sep='\n----------------------\n'
    )
    await message.answer(text.as_html())

@user_private_router.message(F.text.lower().contains('опрос'))
async def opros(message: types.Message):
    await message.reply("опрос:", reply_markup=reply.test_kb)


@user_private_router.message(F.contact)
async def get_contact(message: types.Message):
    await message.answer(f"номер получен")
    await message.answer(str(message.contact))


@user_private_router.message(F.location)
async def get_location(message: types.Message):
    await message.answer(f"локация получена")
    await message.answer(str(message.location))
