from datetime import datetime

from lark_bot_demo.util.card import card_header_builder, button_field_builder


def lipsum_card(content: str):
    return {
        "header": card_header_builder(f"Lipsum: {datetime.now():%Y-%m-%d %H:%M:%S}", "blue"),
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": content
                }
            },
            {
                "tag": "hr"
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "Operate card immediately."
                }
            },
            button_field_builder([
                {
                    "text": "Refresh 1",
                    "style": "success",
                    "data": {"category": "lipsum", "action": "refresh", "data": {"lines": 1}}
                },
                {
                    "text": "Refresh 5",
                    "style": "success",
                    "data": {"category": "lipsum", "action": "refresh", "data": {"lines": 5}}
                },
                {
                    "text": "New 1",
                    "style": "danger",
                    "data": {"category": "lipsum", "action": "new", "data": {"lines": 1}}
                },
                {
                    "text": "New 5",
                    "style": "danger",
                    "data": {"category": "lipsum", "action": "new", "data": {"lines": 5}}
                },
            ]),
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "New card with delay 5s"
                }
            },
            button_field_builder([
                {
                    "text": "New 1",
                    "style": "danger",
                    "data": {"category": "lipsum", "action": "new", "async": True,
                             "data": {"lines": 1, "delay": 5}}
                },
                {
                    "text": "New 5",
                    "style": "danger",
                    "data": {"category": "lipsum", "action": "new", "async": True,
                             "data": {"lines": 5, "delay": 5}}
                },
            ])
        ]
    }
