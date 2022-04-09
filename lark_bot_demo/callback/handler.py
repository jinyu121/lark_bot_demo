import json
import logging
import traceback
from typing import Dict

from flask import copy_current_request_context
from flask import current_app, g
from flask_babel import gettext
from flaskthreads import AppContextThread
from larksuiteoapi.card import Card
from larksuiteoapi.service.im.v1 import MessageReceiveEvent

from lark_bot_demo.callback.impl_card import IdleCardImpl, LipsumCardImpl
from lark_bot_demo.callback.impl_message import CommandMessageImpl, NormalMessageImpl
from lark_bot_demo.db import LarkMessage
from lark_bot_demo.util.helper import MessageHelper
from lark_bot_demo.util.text import text_without_at_user
from lark_bot_demo.util.util import register

_IMPL_CATEGORY = {}  # register card impls here
register(_IMPL_CATEGORY, LipsumCardImpl, "lipsum")


class CallbackEntry:
    def __init__(self, event, user_id: str):
        # Message callback and card callback have different protocol/format.
        # To make things simpler, we record the user_id here, and put the callback data into `g.event`
        self.user_id = user_id
        g.event = event

    def is_duplicated_callback(self, message_id: str) -> bool:
        try:  # To prevent blocking. If de-duplicate fails, the following process should continue
            if LarkMessage.objects(message_id=message_id).first():
                logging.info(f"Duplicated message: {message_id}")
                return True
            elif not current_app.config["DEBUG"]:
                LarkMessage(message_id=message_id).save()
        except:
            traceback.print_exc()

        return False

    def handle(self):
        return NotImplemented


class MessageCallbackEntry(CallbackEntry):
    def __init__(self, event: MessageReceiveEvent):
        super().__init__(event, event.event.sender.sender_id.open_id)
        g.event.event.message.content = json.loads(g.event.event.message.content)

    def handle(self):
        message = g.event.event.message

        # Filter out duplicated messages
        if self.is_duplicated_callback(message.message_id):
            return

        try:
            impl_clazz = NormalMessageImpl

            if "text" == message.message_type \
                    and text_without_at_user(message.content["text"]).startswith("/"):
                impl_clazz = CommandMessageImpl

            impl_clazz().do()

        except Exception as e:
            traceback.print_exc()
            MessageHelper.reply_text(g.event.event.message.message_id, f"ERROR: {e}")

    def idle(self):
        MessageHelper.reply_text(g.event.event.message.message_id, gettext("TEXT_GENERAL_USAGE"))


class CardCallbackEntry(CallbackEntry):
    def __init__(self, event: Card):
        super().__init__(event, event.open_id)

    def handle(self) -> Dict:
        impl = _IMPL_CATEGORY.get(g.event.action.value.get("category"), IdleCardImpl)
        args = [
            g.event.action.value.get("action"),
            g.event.action.option,
            g.event.action.value.get("data", {})
        ]

        try:
            if g.event.action.value.get("async", False):
                # Copy app context and request context to thread
                AppContextThread(target=copy_current_request_context(impl().do), args=args).start()
                return {}
            else:
                return impl().do(*args)
        except Exception as e:
            MessageHelper.reply_text(g.event.open_message_id, f"ERROR: {e}")
            return {}
