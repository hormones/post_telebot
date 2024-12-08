import json
import logging
from typing import cast
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from base.types import Post
import db, config
from buttons import approve

_confirm = "initiate-confirm"
_cancel = "initiate-cancel"


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
    user_id = update.callback_query.from_user.id
    msg_id = param.get("msg_id")
    await update.callback_query.edit_message_text("Post confirmed!")

    post = db.post_query_by_message_id(msg_id)
    if not post:
        logging.error(f"post not found: {user_id}-{msg_id}")
        return
    msg_id = post.message_id
    user_id = post.from_id

    try:
        # copy text message to approve channel
        if not post.media_group_id:
            await context.bot.copy_message(
                chat_id=config.APPROVE_CHANNEL,
                from_chat_id=user_id,
                message_id=msg_id,
                reply_markup=await approve.get_markup(post.message_id),
            )
        else:
            # copy media messages to approve channel
            # attention: wait for 10 seconds to avoid some messages not received
            context.job_queue.run_once(
                callback=media_group_sender,
                when=4,
                data=post,
                name=str(post.media_group_id),
            )
    except Exception as e:
        logging.error(f"Error forward message: {user_id} {msg_id} {e}")


async def media_group_sender(context: ContextTypes.DEFAULT_TYPE):
    post = cast(Post, context.job.data)

    if not post.is_batch:
        await context.bot.copy_message(
            chat_id=config.APPROVE_CHANNEL,
            from_chat_id=post.from_id,
            message_id=post.message_id,
            reply_markup=await approve.get_markup(post.message_id),
        )
    else:
        message_ids = await context.bot.copy_messages(
            chat_id=config.APPROVE_CHANNEL,
            from_chat_id=post.from_id,
            message_ids=post.get_message_ids,
        )
        # add reply_markup by reply
        await context.bot.send_message(
            chat_id=config.APPROVE_CHANNEL,
            reply_to_message_id=message_ids[0].message_id,
            text="approve?",
            reply_markup=await approve.get_markup(post.message_id),
        )
        # add reply_markup for group messages is not working, because telegram is not support until now
        # await context.bot.edit_message_caption(
        #     chat_id=APPROVE_CHANNEL,
        #     message_id=message_ids[0].message_id,
        #     caption="222",
        #     reply_markup=await approve.get_markup(post.message_id),
        # )
