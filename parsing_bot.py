from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests, os, logging


load_dotenv('.env')

bot = Bot(os.environ.get('token2'))
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer("Hellow World")

@dp.message_handler(commands = 'news')
async def get_news(message:types.Message):
    url = "https://akipress.org/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('a', class_='newslink')
    n = 0
    for news in quotes:
        n += 1
        link = news.get('href')
        with open('parsing.txt', 'a+', encoding="utf-8") as file:
            file.write(f"{n}) {news.text}\n")
            await message.answer(f"{n}) {news.text}\n{link}")

@dp.message_handler(commands = 'products')
async def get_products(message:types.Message):
    await message.reply("hhh")
    url = "https://globus-online.kg/catalog/ovoshchi_frukty_orekhi_zelen/ovoshchi/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('div', class_= 'list-showcase__part-main')
    n = 0
    for prod in quotes:
        n += 1
        title = prod.find('div', class_='list-showcase__name')
        price = prod.find('span', class_='c-prices__value js-prices_pdv_ГЛОБУС Розничная')
        await message.answer(f"{n}) {title.text}\n{price.text}")

executor.start_polling(dp)