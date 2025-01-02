import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram bot token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# List of group chat IDs
GROUP_CHAT_IDS = ['@example1' , '@example2']

# List of group chat invite links
GROUP_CHAT_LINKS = ['https://t.me/example1','https://t.me/example2']

# Unique start commands for each media file
MEDIA_COMMANDS = {
    'media1': 'media/media1.jpg',  # Example: {'unique_command': 'path/to/media'}
    'media2': 'media/media2.mp4'
}

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Commands to receive your media:\n'
        + '\n'.join([f'/{cmd}' for cmd in MEDIA_COMMANDS.keys()])
    )

# Function to check if user is in group
async def check_user_in_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    try:
        for chat_id in GROUP_CHAT_IDS:
            member = await context.bot.get_chat_member(chat_id=chat_id, user_id=user_id)
            if member.status in ['member', 'administrator', 'creator']:
                return True
    except Exception as e:
        logger.error(f"Error checking group membership: {e}")
    return False

# Dynamic media handler
async def send_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cmd = update.message.text[1:]  
    media_path = MEDIA_COMMANDS.get(cmd)

    if await check_user_in_group(update, context):
        if media_path:
            if media_path.endswith(('.jpg', '.png', '.jpeg')):
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(media_path, 'rb'))
            elif media_path.endswith(('.mp4', '.mov')):
                await context.bot.send_video(chat_id=update.effective_chat.id, video=open(media_path, 'rb'))
            else:
                await update.message.reply_text('Unsupported media type.')
        else:
            await update.message.reply_text('Invalid command.')
    else:
        keyboard = [
            [InlineKeyboardButton('Join Group', url=url)] for url in GROUP_CHAT_LINKS
        ]
        keyboard.append([InlineKeyboardButton('Check Membership', callback_data='check_membership')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Please join the following group to receive the media:', reply_markup=reply_markup)

# Check membership handler
async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if await check_user_in_group(update, context):
        await query.edit_message_text(text="You are now a member. You can use the commands to receive your media.")
    else:
        await query.edit_message_text(text="You are not a member yet. Please join the group to receive the media.")

# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.warning(f"Update {update} caused error {context.error}")

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(check_membership, pattern='check_membership'))
    # Add handlers for each unique media command
    for cmd in MEDIA_COMMANDS.keys():
        application.add_handler(CommandHandler(cmd, send_media))
    application.add_error_handler(error)

    application.run_polling()

if __name__ == '__main__':
    main()
