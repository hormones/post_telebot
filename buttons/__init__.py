import json
import logging
from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from buttons import initiate, approve
from config import APP

_buttons = {
    "initiate": initiate.handle,
    "approve": approve.handle,
}


# This callback is triggered when a button is pressed
async def _button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    from_user = update.callback_query.from_user
    await query.answer()  # Acknowledge the button press

    logging.info(
        f"button pressed by user: {from_user.username}[{from_user.id}], data: {query.data}"
    )
    if not query.data:
        return

    param = json.loads(query.data)
    button_key: str = param.get("key")

    for key in _buttons:
        if button_key.startswith(key):
            await _buttons[key](param, update, context)
            break
    else:
        raise ValueError(f"unknown key: {button_key}")


async def init():
    APP.add_handler(CallbackQueryHandler(_button_callback))
    logging.info("=== buttons initialized ===")
