import requests
from bs4 import BeautifulSoup
from telegram import Bot, error
import asyncio
import time
from datetime import datetime, time as dtime

# Telegram bot token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = Bot(token=TOKEN)

# Group chat ID
GROUP_CHAT_ID = '@YOUR_GROUP_CHAT_ID'

# URL to scrape
URL = 'https://www.tgju.org/profile/price_dollar_rl'

# Time to send the highest and lowest prices (24-hour format)
SEND_TIME = dtime(0, 0)  # 00:00


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
    await bot.send_message(
        chat_id=GROUP_CHAT_ID, text=f"💸قیمت لحظه ای : \n{price} ريال"
    )


async def send_daily_summary(highest_price, lowest_price):
    text = (
        f"💸بالاترین قیمت روز:\n {highest_price} ريال\n"
        f"💸پایین ترین قیمت روز:\n {lowest_price} ريال"
    )
    await bot.send_message(chat_id=GROUP_CHAT_ID, text=text)


async def main():
    if not check_telegram_connection():
        return
    highest_price = None
    lowest_price = None
    last_price = None

    while True:
        try:
            current_price = get_price()
            if current_price:
                if last_price is None or current_price != last_price:
                    await send_message(current_price)
                    last_price = current_price
                current_price_value = int(current_price.replace(',', ''))
                # Update highest and lowest prices
                if highest_price is None or current_price_value > int(
                    highest_price.replace(',', '')
                ):
                    highest_price = current_price
                if lowest_price is None or current_price_value < int(
                    lowest_price.replace(',', '')
                ):
                    lowest_price = current_price
            now = datetime.now().time()
            if now >= SEND_TIME and now < (SEND_TIME.replace(minute=1)):
                await send_daily_summary(highest_price, lowest_price)
                highest_price = None
                lowest_price = None
                await asyncio.sleep(
                    60
                )  # Wait for 60 seconds to ensure it doesn't repeat
            await asyncio.sleep(600)  # Check the price every second
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    asyncio.run(main())
