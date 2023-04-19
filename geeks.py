from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
import logging
import os
import asyncio
import aioschedule

load_dotenv('.env')

bot = Bot(os.environ.get('token'))
dp = Dispatcher(bot, storage=MemoryStorage())
storage = MemoryStorage()
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
        await enroll_get(call.message)

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

class EnrollState(StatesGroup):
    data = State()

@dp.message_handler(commands=['enroll'])
async def enroll_get(message:types.Message):
    await message.reply("Оставьте свои контакты в формате: имя, фамилия и номер\nИ мы скоро с вами свяжемся")
    await EnrollState.data.set()

@dp.message_handler(state=EnrollState.data)
async def send_enroll(message:types.Message, state:FSMContext):
    print(message.text)
    await bot.send_message(-964627083, f"Заявка на курсы:\n{message.text}")
    await message.answer('Спасибо ваши данные успешно записаны')
    await state.finish()

async def send_message():
    await bot.send_message(-964627083, "Здраствуйте, у вас сегодя урок в 20:00")

async def scheduler():
    # aioschedule.every().day.at("12:00").do(send_message)
    aioschedule.every(5).seconds.do(send_message)
    # aioschedule.every().wednesday.at('21:08').do(send_message)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(_):
    asyncio.create_task(scheduler())

@dp.message_handler()
async def nothing(message:types.Message):
    await message.answer('')
    
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)