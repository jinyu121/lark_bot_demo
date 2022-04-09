from typing import Dict, List


def card_header_builder(title: str, template: str = ""):
    conf = {
        "title": {
            "content": title,
            "tag": "plain_text"
        }
    }
    if template:
        conf["template"] = template
    return conf


def text_choice_field_builder(text: str, current: str, callback_value: Dict, options: List):
    callback_value.setdefault("data", {})
    option_ui = []

    for option in options:
        option_ui.append(
            {
                "text": {
                    "tag": "plain_text",
                    "content": option["key"]
                },
                "value": option["value"]
            }
        )

    conf = {
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": text
        },
        "extra": {
            "tag": "select_static",
            "placeholder": {
                "tag": "plain_text",
                "content": current
            },
            "value": callback_value,
            "options": option_ui
        }
    }

    return conf


def text_button_field_builder(text: str, btn: str, url: str = "", data: Dict = None, style: str = "primary"):
    conf = {
        "extra": {
            "tag": "button",
            "text": {
                "content": btn,
                "tag": "lark_md"
            },
            "type": style
        },
        "tag": "div",
        "text": {
            "content": text,
            "tag": "lark_md"
        }
    }
    if url:
        conf["extra"]["url"] = url
    elif data:
        conf["extra"]["value"] = data

    return conf


def button_field_builder(data: List[Dict]):
    actions = []
    for btn in data:
        b = {
            "tag": "button",
            "text": {
                "tag": "plain_text",
                "content": btn["text"]
            },
            "type": btn.get("style"),
        }
        if btn.get("url"):
            b["url"] = btn["url"]
        elif btn.get("data"):
            b["value"] = btn["data"]

        actions.append(b)

    return {
        "tag": "action",
        "actions": actions
    }
