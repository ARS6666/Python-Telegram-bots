import logging
import random
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram bot token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'


# Command functions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Hello! I am your friendly bot. Type /help to see what I can do!'
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Here are some commands you can use:\n'
        '/start - Start the bot\n'
        '/help - Get help\n'
        '/funfact - Get a fun fact\n'
        '/joke - Get a joke\n'
        '/echo - Echo your message'
    )


async def fun_fact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    facts = [
        'Honey never spoils.',
        'A single strand of spaghetti is called a spaghetto.',
        'Octopuses have three hearts.',
        "Bananas are berries, but strawberries aren't."
    ]
    await update.message.reply_text(f"Fun Fact: {random.choice(facts)}")


async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        'Why did the scarecrow win an award? Because he was outstanding in his field!',
        "Why don't skeletons fight each other? They don't have the guts."
    ]
    await update.message.reply_text(f"Joke: {random.choice(jokes)}")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)


# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.warning(f"Update {update} caused error {context.error}")


def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('funfact', fun_fact))
    application.add_handler(CommandHandler('joke', joke))
    application.add_handler(CommandHandler('echo', echo))
    application.add_error_handler(error)

    application.run_polling()


if __name__ == '__main__':
    main()
