import random
import requests
from telegram import Update, BotCommand
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext
)

# Your bot token from BotFather
BOT_TOKEN = 'YOUR-BOT-TOKEN-HERE'

async def is_owner_or_admin(update: Update) -> bool:
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    chat_member = await update.effective_chat.get_member(user_id)
    return chat_member.status in ['administrator', 'creator']

# Start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        'سلام! من ربات ادمین شما هستم. برای مشاهده دستورات از /help استفاده کنید.'
    )

# Help command
async def help_command(update: Update, context: CallbackContext) -> None:
    commands = [
        '/start - شروع',
        '/help - راهنما',
        '/mute - بی‌صدا کردن کاربر',
        '/unmute - برداشتن بی‌صدا',
        '/kick - اخراج کاربر',
        '/ban - مسدود کردن کاربر',
        '/unban - رفع مسدودیت',
    ]
    await update.message.reply_text('\n'.join(commands))

# Mute command
async def mute(update: Update, context: CallbackContext) -> None:
    if not await is_owner_or_admin(update):
        await update.message.reply_text('فقط صاحب گروه و ادمین‌ها توانایی این کار را دارند!')
        return

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await context.bot.restrict_chat_member(
            chat_id=update.message.chat_id, user_id=user_id, permissions={'can_send_messages': False}
        )
        await update.message.reply_text('کاربر بی‌صدا شد.')

# Unmute command
async def unmute(update: Update, context: CallbackContext) -> None:
    if not await is_owner_or_admin(update):
        await update.message.reply_text('فقط صاحب گروه و ادمین‌ها توانایی این کار را دارند!')
        return

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await context.bot.restrict_chat_member(
            chat_id=update.message.chat_id, user_id=user_id, permissions={'can_send_messages': True}
        )
        await update.message.reply_text('بی‌صدا برداشته شد.')

# Kick command
async def kick(update: Update, context: CallbackContext) -> None:
    if not await is_owner_or_admin(update):
        await update.message.reply_text('فقط صاحب گروه و ادمین‌ها توانایی این کار را دارند!')
        return

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await context.bot.ban_chat_member(chat_id=update.message.chat_id, user_id=user_id)
        await update.message.reply_text('کاربر اخراج شد.')

# Ban command
async def ban(update: Update, context: CallbackContext) -> None:
    if not await is_owner_or_admin(update):
        await update.message.reply_text('فقط صاحب گروه و ادمین‌ها توانایی این کار را دارند!')
        return

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await context.bot.ban_chat_member(
            chat_id=update.message.chat_id, user_id=user_id
        )
        await update.message.reply_text('کاربر مسدود شد.')

# Unban command
async def unban(update: Update, context: CallbackContext) -> None:
    if not await is_owner_or_admin(update):
        await update.message.reply_text('فقط صاحب گروه و ادمین‌ها توانایی این کار را دارند!')
        return

    if len(context.args) > 0:
        user_id = context.args[0]
        await context.bot.unban_chat_member(chat_id=update.message.chat_id, user_id=user_id)
        await update.message.reply_text('کاربر رفع مسدودیت شد.')

# Fun responses
async def fun_responses(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text.lower()
    fun_replies = {
        'سلام': ['سلام! چطورید؟', 'درود بر شما!', 'سلام سلام!'],
        'خوبی': ['من خوبم، شما چطورید؟', 'خیلی خوب، شما چطورید؟'],
        'چه خبر': ['همه چی آرومه، شما چطورید؟', 'خبر خاصی نیست، شما چه خبر؟'],
        'خداحافظ': ['خدانگهدار! مواظب خودتون باشید.', 'خداحافظ! تا بعد.']
    }

    for key, value in fun_replies.items():
        if key in user_message:
            await update.message.reply_text(random.choice(value))
            break

def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('mute', mute))
    application.add_handler(CommandHandler('unmute', unmute))
    application.add_handler(CommandHandler('kick', kick))
    application.add_handler(CommandHandler('ban', ban))
    application.add_handler(CommandHandler('unban', unban))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fun_responses))

    application.run_polling()

if __name__ == '__main__':
    main()
