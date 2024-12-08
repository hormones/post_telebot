import logging

from telegram import Update
from telegram.ext import filters, ContextTypes, MessageHandler

from base.types import Post
from config import APP
from base import util
from buttons import initiate
import db


async def init():
    APP.add_handler(MessageHandler(filters.ChatType.PRIVATE, _handle))
    logging.info(f"=== post initialized ===")


async def _handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from_user = update.message.from_user
    message_id = update.message.message_id
    media_group_id = update.message.media_group_id

    logging.info(
        f"new message({message_id})({media_group_id}) from {from_user.username}({from_user.id})"
    )

    # store post
    post = Post(
        media_group_id=media_group_id, from_id=from_user.id, message_id=message_id
    )
    db.post_insert(post)

    handled = media_group_id is not None and not util.cache_ttl_if_absent(
        media_group_id, message_id
    )
    if handled:
        return
    await _handle_reply(update, context)


async def _handle_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # log user`s input
    media_group_id = update.message.media_group_id
    message_text = update.message.text
    if media_group_id is not None:
        if message_text is None:
            message_text = update.message.caption
    logging.info(f"new message with text: {message_text}")
    mark_up = await initiate.get_markup(update.message.message_id)
    await update.message.reply_text(
        "Got it!", reply_to_message_id=update.message.message_id, reply_markup=mark_up
    )
