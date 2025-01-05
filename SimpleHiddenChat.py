import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram bot token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Stores user chat states and anonymous chat IDs
anonymous_chats = {}


# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if args:
        recipient_id = args[0]
        user_id = update.message.from_user.id

        anonymous_chats[user_id] = recipient_id
        anonymous_chats[recipient_id] = user_id

        await update.message.reply_text(
            'You are now connected anonymously. You can start messaging.'
        )
        context.user_data['anonymous_chat'] = True
    else:
        await update.message.reply_text(
            'Hello! I am your anonymous chat bot. Use /help to see available commands.'
        )


# Help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Available commands:\n'
        '/start [link] - Start the bot or connect with someone anonymously\n'
        '/help - Get help\n'
        '/link - Get your unique bot link\n'
        '/cancel - Cancel the current operation'
    )


# Generate link command handler
async def link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    bot_link = f"https://t.me/UpdateDollarPriceBot?start={user_id}"
    await update.message.reply_text(f"Your unique bot link: {bot_link}")


# Handle anonymous messages
async def handle_anonymous_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    user_id = update.message.from_user.id
    recipient_id = anonymous_chats.get(user_id)
    message_id = update.message.message_id

    if recipient_id:
        # Add reveal button
        reveal_button = InlineKeyboardButton(
            'Reveal Reply Link',
            callback_data=f"reveal_{user_id}_{message_id}_{update.message.text}"
        )
        keyboard = InlineKeyboardMarkup([[reveal_button]])

        await context.bot.send_message(
            chat_id=recipient_id,
            text='You have received an anonymous message.',
            reply_markup=keyboard
        )
        await update.message.reply_text('Message sent anonymously.')
    else:
        await update.message.reply_text('Error: Anonymous chat not found.')


# Reveal reply link handler
async def reveal_reply_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    query_data = query.data.split('_')

    if query_data[0] == 'reveal':
        user_id = int(query_data[1])
        message_id = int(query_data[2])
        message_text = '_'.join(query_data[3:])
        recipient_id = anonymous_chats.get(user_id)

        if recipient_id:
            reply_link = f"https://t.me/UpdateDollarPriceBot?start={user_id}&reply_to={message_id}"
            new_message_text = f"{message_text}\n\n[Reply]({reply_link})"
            await context.bot.send_message(
                chat_id=recipient_id, text=new_message_text, parse_mode='Markdown'
            )
            await query.answer('Reply link revealed.')

            # Delete the reveal button message
            await context.bot.delete_message(
                chat_id=recipient_id, message_id=query.message.message_id
            )
        else:
            await query.answer('Error: Anonymous chat not found.')


# Cancel command handler
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    recipient_id = anonymous_chats.get(user_id)

    if recipient_id:
        await context.bot.send_message(
            chat_id=recipient_id, text='Anonymous chat ended.'
        )
        del anonymous_chats[user_id]
        del anonymous_chats[recipient_id]
    await update.message.reply_text('Anonymous chat canceled.')
    return ConversationHandler.END


# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.warning(f"Update {update} caused error {context.error}")


def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('link', link))
    application.add_handler(CommandHandler('cancel', cancel))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_anonymous_message)
    )
    application.add_handler(CallbackQueryHandler(reveal_reply_link))
    application.add_error_handler(error)

    application.run_polling()


if __name__ == '__main__':
    main()
