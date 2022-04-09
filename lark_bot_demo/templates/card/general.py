from lark_bot_demo.util.card import card_header_builder


def general_card(content: str, header: str = "", template: str = ""):
    data = {
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": content
                }
            }
        ]
    }
    if header:
        data["header"] = card_header_builder(header, template)

    return data
