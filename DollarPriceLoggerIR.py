import requests
from bs4 import BeautifulSoup
from telegram import Bot
import asyncio
import time

# Telegram bot token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = Bot(token=TOKEN)

# Group chat ID
GROUP_CHAT_ID = '@YOUR_GROUP_CHAT_ID'

# URL to scrape
URL = 'https://www.tgju.org/profile/price_dollar_rl'


def check_telegram_connection():
    try:
        bot.get_me()
        print('Successfully connected to Telegram!')
        return True
    except Exception as e:
        print(f"Failed to connect to Telegram: {e}")
        return False


def get_price():
    retries = 3
    while retries > 0:
        try:
            response = requests.get(URL, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            price_element = soup.find('span', {'data-col': 'info.last_trade.PDrCotVal'})
            if price_element:
                return price_element.text.strip()
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            retries -= 1
            time.sleep(1)
    return None


async def send_message(price):
    print(price)
    await bot.send_message(chat_id=GROUP_CHAT_ID, text=f"قیمت دلار: {price}")


async def main():
    if not check_telegram_connection():
        return
    last_price = None
    while True:
        try:
            current_price = get_price()
            if current_price and current_price != last_price:
                await send_message(current_price)
                last_price = current_price
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    asyncio.run(main())
