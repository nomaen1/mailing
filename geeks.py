from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters.state import StatesGroup,State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
import sqlite3
import logging
import os

load_dotenv('.env')

bot = Bot(os.environ.get('token'))
dp = Dispatcher(bot,storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

buttons = [
    InlineKeyboardButton('Backend', callback_data='Backend'),
    InlineKeyboardButton('Frontend', callback_data='Frontend'),
    InlineKeyboardButton('Ux/Ui', callback_data='ux/ui'),
    InlineKeyboardButton('Android-разработка', callback_data='Android'),
    InlineKeyboardButton('IOS-разработка', callback_data='ios'),
]
button = InlineKeyboardMarkup().add(*buttons)

enroll = [
    InlineKeyboardButton('Записаться', callback_data='enroll_student'),
    InlineKeyboardButton('Адрес', url='https://go.2gis.com/vmxby')
]

enroll_button = InlineKeyboardMarkup().add(*enroll)

num_button = [
    KeyboardButton('Подтвердить номер', request_contact=True)
]

number = ReplyKeyboardMarkup(resize_keyboard=True).add(*num_button)

@dp.message_handler(commands=["start"])
async def start(message:types.Message):
    await message.answer("Приветствую! Я бот который предоставит вам базовую информацию об IT-курсах в Geeks.")
    await message.answer('Существуют 5 направлений. Для подробной информации о каждом нажмите на соответствующую кнопку.', reply_markup=button)

@dp.callback_query_handler(lambda call:call)
async def inline(call):
    if call.data == 'Backend':
        await back(call.message)
    elif call.data == 'Frontend':
        await front(call.message)
    elif call.data == 'ux/ui':
        await uxui(call.message)
    elif call.data == 'Android':
        await android(call.message)
    elif call.data == 'ios':
        await ios(call.message)
    elif call.data == 'enroll_student':
        await get_enrolled(call.message)

class BackendCourse(StatesGroup):
    backend = State()

@dp.message_handler(commands=['backend'])
async def back(message:types.Message):
    await message.answer('Бэкенд – это внутренняя, скрытая от пользователя начинка сайта или веб-приложения. Другими словами, это часть сервиса, которая работает на удаленном сервере, а не в браузере или персональном компьютере.')
    await message.answer('Стоимость обучения: 10.000 сом в месяц.')
    await message.answer('Срок обучения: 5 месяцев.', reply_markup=enroll_button)

@dp.message_handler(commands=['frontend'])
async def front(message:types.Message):
    await message.answer('Фронтенд-разработка — это создание пользовательского интерфейса на клиентской стороне веб‑сайта или приложения. Это всё, что видит пользователь, когда открывает веб-страницу, и с чем он взаимодействует: кнопки, баннеры и анимация.')
    await message.answer('Стоимость обучения: 15.000 сом в месяц.')
    await message.answer('Срок обучения: 5 месяцев.', reply_markup=enroll_button)

@dp.message_handler(commands=['ux/ui'])
async def uxui(message:types.Message):
    await message.answer('UX/UI-дизайнер ― одна из самых востребованных  профессий на рынке. В этом материале мы подробно разбираем, кто такой UX/UI-дизайнер и почему UX/UI-дизайн ― не только про графику.')
    await message.answer('Стоимость обучения: 11.000 сом в месяц.')
    await message.answer('Срок обучения: 3 месяцев.', reply_markup=enroll_button)

@dp.message_handler(commands=['android'])
async def android(message:types.Message):
    await message.answer('Андроид-разработчик создаёт приложения и поддерживает их работу, продумывает интерфейс и логику, изучает пользовательские пожелания и делает обновления.')
    await message.answer('Стоимость обучения: 8.000 сом в месяц.')
    await message.answer('Срок обучения: 7 месяцев.', reply_markup=enroll_button)

@dp.message_handler(commands=['ios'])
async def ios(message:types.Message):
    await message.answer('Разработка приложений для iOS — это процесс создания мобильных приложений для оборудования Apple, включая iPhone, iPad и iPod Touch. Программное обеспечение написано на языке программирования Swift, а затем развернуто в App Store для загрузки пользователями.')
    await message.answer('Стоимость обучения: 8.000 сом в месяц.')
    await message.answer('Срок обучения: 7 месяцев.', reply_markup=enroll_button)

@dp.message_handler(commands='enroll')
async def get_enrolled(message:types.Message):
    await message.answer('Отправьте свои данные: фамилия,  имя, номер телефона')
    await BackendCourse.backend.set()


@dp.message_handler(state=BackendCourse.backend)
async def course_pon(message:types.Message, state : FSMContext ):
    id_chat = "-964627083"
    try:
        await bot.send_message(chat_id=int(id_chat), text=message.text)
        await state.finish()

    except:
        await message.answer("Произашла ошибка")
        await state.finish()

executor.start_polling(dp)
