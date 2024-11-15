from telegram import BotCommand, Update
from telegram.ext import ContextTypes, CommandHandler

NAME = "end"
BOT_COMMAND = BotCommand(command=NAME, description="End with the bot")
BOT_HANDLER = CommandHandler(NAME, lambda u, c: handler(u, c))


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{NAME}!")
