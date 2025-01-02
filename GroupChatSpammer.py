import asyncio
from telegram import Bot

# Telegram bot token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = Bot(token=TOKEN)

# Group chat ID
CHAT_ID = 'YOUR-TARGET-GROUP-CHAT-ID'

SPAM_MESSAGE = 'Test'


# Function to send message to Telegram group or user
async def send_message():
    try:
        await bot.send_message(chat_id=CHAT_ID, text=SPAM_MESSAGE)
        print(f"Message sent: {SPAM_MESSAGE}")
    except Exception as e:
        print(f"Failed to send message: {e}")


# Main loop to send message every 1 seconds
async def main():
    while True:
        await send_message()
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
