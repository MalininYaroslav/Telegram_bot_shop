import asyncio
import logging
from random import randint
from aiogram import Bot, Dispatcher, types
from yoomoney import Quickpay, Client

def len(self):
    counter=0
    for sub in self.operations:
        counter+=1
    return counter 

logging.basicConfig(level=logging.INFO)

TOKEN_TG = 'YOUR TOKEN'
TOKEN_YOO = 'YOUR TOKEN'

Label = None
if Label is None:
    Label=randint(-10e16,10e16)

client = Client(TOKEN_YOO)
bot = Bot(token=TOKEN_TG)
dp = Dispatcher(bot)
quickpay_privat = Quickpay(
    receiver="YOUR ACCOUNT",
    quickpay_form="shop",
    targets="Оплата доступа к приватному каналу",
    paymentType="SB",
    sum=2000,
    label=Label
)
quickpay_vip = Quickpay(
    receiver="YOUR ACCOUNT",
    quickpay_form="shop",
    targets="Оплата доступа к приватному каналу",
    paymentType="SB",
    sum=1000,
    label=Label
)


@dp.message_handler(commands="start")
async def command_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text='💰Купить доступ'),
            types.KeyboardButton(text='⚙️Тех. поддержка')
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Выберите действие'
    )
    await message.answer(
        f'Привет, {message.from_user.first_name}! Это бот для получения доступа в приватный канал Eva Gold! Нажмите кнопку "Купить доступ" для получения доступа в канал. Если остались какие-то вопросы, то нажмите "Тех. поддержка"',
        reply_markup=keyboard
    )


@dp.message_handler(text='💰Купить доступ')
async def buying_access(message: types.Message):
    if len(client.operation_history(label=Label)) == 0:
        kb = [
            [types.InlineKeyboardButton(text='Оплатить🤑', url=quickpay_privat.base_url)]
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
        await message.answer(
            'К оплате 2000 рублей.\nДля оплаты нажмите "Оплатить".',
            reply_markup=keyboard
        )
        kb = [
            [types.KeyboardButton(text='Проверить оплату✅'),
             types.KeyboardButton(text='Назад⬅️')
             ]
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True
        )
        await message.answer(
            'После оплаты нажмите "Проверить оплату", чтобы проверить прошла ли оплата. Если все прошло успешно Вам придет ссылка на вступление в канал.\n\nИли нажмите "Назад", чтобы вернуться в главное меню.',
            reply_markup=keyboard
        )
    elif len(client.operation_history(label=Label)) == 1:
        kb = [
            [types.InlineKeyboardButton(text='Оплатить🤑', url=quickpay_vip.base_url)]
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
        await message.answer(
            'У вас уже есть доступ к закрытому каналу. Вы можете получить доступ к VIP каналу за 1000 рублей.',
            reply_markup=keyboard
        )
        kb = [
            [types.KeyboardButton(text='Назад⬅️')]
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True
        )
        await message.answer(
            'Или нажмите "Назад", чтобы вернуться в главное меню.',
            reply_markup=keyboard
        )
    elif len(client.operation_history(label=Label)) == 2:
        kb = [
            [types.KeyboardButton(text='Назад⬅️')]
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True
        )
        await message.answer(
            'У вас уже максимальный уровень доступа!',
            reply_markup=keyboard
        )


@dp.message_handler(text='Проверить оплату✅')
async def Check_operation(message: types.Message):
    if len(client.operation_history(label=Label)) == 0:
        await message.answer(
            'Произошла ошибка! Оплатите и нажмите снова "Проверить оплату"'
        )
    elif len(client.operation_history(label=Label)) == 1:
        kb = [
            [types.InlineKeyboardButton(text='Вступить в канал', url='YOUR TG-CHANNEL')]
        ]
        keyboard = types.InlineKeyboardMarkup(
            inline_keyboard=kb
        )
        await message.answer(
            'Оплата прошла успешно!\n Нажмите "Вступить в канал", для доступа к контенту.',
            reply_markup=keyboard
        )
        kb = [
            [types.KeyboardButton(text='Назад⬅️')]
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True
        )
        await message.answer(
            'А также можете приобрести доступ в VIP канал нажатием кнопки "Купить доступ" еще раз.\n\nДля этого нажмите "Назад", затем "Купить доступ"',
            reply_markup=keyboard
        )
    elif len(client.operation_history(label=Label)) == 2:
        kb = [
            [types.InlineKeyboardButton(text='Вступить в канал', url='YOUR TG-CHANNEL')]
        ]
        keyboard = types.InlineKeyboardMarkup(
            inline_keyboard=kb
        )
        await message.answer(
            'Оплата прошла успешно!\n Нажмите "Вступить в канал", для доступа к контенту.',
            reply_markup=keyboard
        )


@dp.message_handler(text='Назад⬅️')
async def back(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text='💰Купить доступ'),
            types.KeyboardButton(text='⚙️Тех. поддержка')
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Выберите действие'
    )
    await message.answer(
        'Вы вернулись в главное меню.',
        reply_markup=keyboard
    )


@dp.message_handler(text='⚙️Тех. поддержка')
async def repair(message: types.Message):
    kb = [
        [types.InlineKeyboardButton(text='Написать', url='YOUR TG-ACCOUNT')]
    ]
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=kb
    )
    await message.answer(
        'Нажмите на кнопку "Написать" и задайте свой впорос.',
        reply_markup=keyboard
    )
    kb = [
        [types.KeyboardButton(text='Назад⬅️')]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    await message.answer(
        'Или нажмите "Назад", чтобы вернуться в главное меню.',
        reply_markup=keyboard
    )


@dp.message_handler()
async def none(message: types.Message):
    await message.answer(
        'Команда не найдена! Введите корректную'
    )


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
