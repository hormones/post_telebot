import logging
from telegram.ext import MessageHandler, filters

from commands import start, begin, end, unknown
from config import APP

_handlers = [
    start.BOT_HANDLER,
    begin.BOT_HANDLER,
    end.BOT_HANDLER,
    MessageHandler(filters.COMMAND, unknown.init),
]
_commands = [start.BOT_COMMAND, begin.BOT_COMMAND, end.BOT_COMMAND]


async def init():
    # add command handlers
    APP.add_handlers(_handlers)
    # register commands
    await APP.bot.set_my_commands(_commands)

    logging.info("=== commands initialized ===")
