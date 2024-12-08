import json
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from base.types import Post
from base import util
import config
import db

_confirm = "approve-confirm"
_cancel = "approve-cancel"


async def get_markup(message_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Confirm",
                    callback_data=json.dumps(
                        {"key": _confirm, "msg_id": message_id}),
                ),
                InlineKeyboardButton(
                    "Cancel",
                    callback_data=json.dumps(
                        {"key": _cancel, "msg_id": message_id}),
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
    msg_id = param.get("msg_id")
    post = db.post_query_by_message_id(msg_id)
    if not post:
        logging.error(f"post not found: {msg_id}")
        return
    approval_ids = None
    # copy user message to display channel
    if not post.is_batch:
        id = await context.bot.copy_message(
            chat_id=config.DISPLAY_CHANNEL,
            from_chat_id=post.from_id,
            message_id=post.message_id,
        )
        approval_ids = str(id.message_id)
    else:
        ids = await context.bot.copy_messages(
            chat_id=config.DISPLAY_CHANNEL,
            from_chat_id=post.from_id,
            message_ids=post.get_message_ids,
        )
        approval_ids = ",".join([str(i.message_id) for i in ids])

    # update post
    up = Post(id=post.id, approval_result=1, approver_id=update.callback_query.from_user.id, approval_ids=approval_ids)
    db.post_update(up)
    logging.info(f"post approved: {util.dumps(up)}")
    await update.callback_query.edit_message_text("Post confirmed.")
