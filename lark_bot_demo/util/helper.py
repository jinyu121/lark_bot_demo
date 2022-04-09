import json
from hashlib import md5
from typing import Dict

from flask import current_app
from larksuiteoapi.service.im.v1 import MessageReplyReqBody
from retry.api import retry_call

from lark_bot_demo.util.const import LARK_UPLOAD_FILE_LIMIT, RETRY_DELAY, RETRY_TIMES_NORMAL


class MessageHelper:
    @classmethod
    def get_message_resource(cls, message_id: str, file_key: str, resource_type: str) -> bytes:
        req = current_app.lark_im \
            .message_resources \
            .get() \
            .set_message_id(message_id) \
            .set_file_key(file_key) \
            .set_type(resource_type)
        rsp = retry_call(req.do, tries=RETRY_TIMES_NORMAL)
        if 0 == rsp.code:
            return rsp.data
        else:
            raise rsp.msg  # Use file error so that ser can see what happened

    @classmethod
    def _reply(cls, message_id: str, msg_type: str, content: Dict):
        body = MessageReplyReqBody()
        body.msg_type = msg_type
        body.content = json.dumps(content)

        req = current_app.lark_im.messages \
            .reply(body=body) \
            .set_message_id(message_id)
        rsp = retry_call(req.do, tries=RETRY_TIMES_NORMAL, delay=RETRY_DELAY)
        if 0 == rsp.code:
            return rsp.data
        else:
            raise f"{rsp.code}: {rsp.msg}"

    @classmethod
    def reply_text(cls, message_id: str, text: str):
        cls._reply(message_id, 'text', {"text": text or " "})

    @classmethod
    def reply_share(cls, message_id: str, user_or_chat_id: str):
        if user_or_chat_id.startswith("oc_"):
            return cls._reply(message_id, 'share_chat', {"chat_id": user_or_chat_id})
        elif user_or_chat_id.startswith("ou_"):
            return cls._reply(message_id, 'share_user', {"user_id": user_or_chat_id})
        else:
            raise f"Unknown id type: {user_or_chat_id}"

    @classmethod
    def reply_image(cls, message_id: str, img: bytes):
        if len(img) >= LARK_UPLOAD_FILE_LIMIT:
            return cls.reply_file(message_id, img, file_type="stream", suffix=".png")
        else:
            file_key = cls.upload_lark(img, file_type="image")
            return cls._reply(message_id, 'image', {"image_key": file_key})

    @classmethod
    def reply_file(cls, message_id: str, data: bytes, file_type: str = "stream", suffix: str = ""):
        file_key = cls.upload_lark(data, file_type, suffix)
        return cls._reply(message_id, 'file', {"file_key": file_key})

    @classmethod
    def reply_card(cls, message_id: str, card_data: Dict):
        return cls._reply(message_id, 'interactive', card_data)

    @classmethod
    def upload_lark(cls, data: bytes, file_type: str, suffix: str = ""):
        if "image" == file_type:
            req = current_app.lark_im.images.create() \
                .set_image_type('message') \
                .set_image(data)
            rsp = retry_call(req.do, tries=RETRY_TIMES_NORMAL, delay=RETRY_DELAY)
            return rsp.data.image_key
        else:
            req = current_app.lark_im.files.create() \
                .set_file_type(file_type) \
                .set_file_name(md5(data).hexdigest() + suffix) \
                .set_file(data)
            rsp = retry_call(req.do, tries=RETRY_TIMES_NORMAL, delay=RETRY_DELAY)
            return rsp.data.file_key
