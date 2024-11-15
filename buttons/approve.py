import json
import logging
from typing import cast
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from base.types import Post
from config import APPROVE_CHANNEL
import db

_confirm = "approve-confirm"
_cancel = "approve-cancel"


async def get_markup(message_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Confirm",
                    callback_data=json.dumps({"key": _confirm, "msg_id": message_id}),
                ),
                InlineKeyboardButton(
                    "Cancel",
                    callback_data=json.dumps({"key": _cancel, "msg_id": message_id}),
                ),
            ]
        ]
    )


async def handle(param: dict, update: Update, context: ContextTypes.DEFAULT_TYPE):
    button_key = param.get("key")
    if button_key == _confirm:
        await _handle_confirm(param, update, context)
    elif button_key == _cancel:
        await _handle_cancel(param, update, context)
    else:
        raise ValueError(f"unknown key: {button_key}")


async def _handle_cancel(
    param: dict, update: Update, context: ContextTypes.DEFAULT_TYPE
):
    await update.callback_query.edit_message_text("Post cancelled.")


async def _handle_confirm(
    param: dict, update: Update, context: ContextTypes.DEFAULT_TYPE
):
    await update.callback_query.edit_message_text("Post confirmed.")
