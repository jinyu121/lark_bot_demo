import logging
from time import sleep
from typing import Dict

from flask import g, current_app

import lark_bot_demo.templates.card.lipsum as lipsum_card_template
from lark_bot_demo.util.helper import MessageHelper


class BaseCardImpl:
    def do(self, action: str, option: str, data: Dict):
        """
        When get callback from card, should set callback value as
        ```
        {
            "category": "some_category",              # Category must register in `card.py`
            "action": "some_action",                  # Will call `do_{some_action}` function
            "async": False,                           # If True, will return immediately
            "data": {                                 # Optional
                "other_variables": "other_values",    # Other values
            }
        }
        ```

        :param action: The function name
        :param option: The user selected value
        :param data: Other data
        :return:
        """

        func = getattr(self, f"do_{action}", self.do_dummy)
        if func is self.do_dummy:
            logging.error(f"Unsupported action `{action}`")

        return func(option, data) or {}

    def do_dummy(self, option: str, data: Dict):
        return {}


class IdleCardImpl(BaseCardImpl):
    def do_dummy(self, option: str, data: Dict):
        MessageHelper.reply_text(g.event.open_message_id, "Dummy")
        return {}


class LipsumCardImpl(BaseCardImpl):
    def do_refresh(self, option: str, data: Dict):
        lines = data.get('lines')

        data = current_app.lipsum.get(lines)
        text = "\n\t".join(data)

        return lipsum_card_template.lipsum_card(text)

    def do_new(self, option: str, data: Dict):
        lines = data.get('lines')
        delay = data.get('delay')

        data = current_app.lipsum.get(lines)
        text = "\n\t".join(data)
        card_data = lipsum_card_template.lipsum_card(text)

        if delay:
            sleep(delay)

        MessageHelper.reply_card(g.event.open_message_id, card_data)

        return {}
