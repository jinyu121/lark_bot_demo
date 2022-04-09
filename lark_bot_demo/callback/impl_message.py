from argparse import ArgumentParser
from time import sleep
from typing import List

from flask import current_app, g

from lark_bot_demo.templates.card.lipsum import lipsum_card
from lark_bot_demo.util.helper import MessageHelper
from lark_bot_demo.util.text import text_without_at_user
from lark_bot_demo.util.util import register


# In this demo, we want to create a "lipsum" bot with these functions:
# 1. "N": Return N paragraphs of lipsum text
# 2. "N M": Sleep for M seconds, and return N sentences of lipsum text
# 3. "N --card": Return N paragraphs of lipsum text, with a card
# 3. "N M --card": Return N paragraphs of lipsum text, with a card


class NormalMessageImpl:
    """
    Normal text message
    """

    def __init__(self, **kwargs):
        pass

    def do(self):
        message_content = g.event.event.message.content
        message_at_list = [u.key for u in g.event.event.message.mentions] if g.event.event.message.mentions else []
        content = text_without_at_user(message_content["text"], message_at_list)

        parser = ArgumentParser()
        parser.add_argument("lines", type=int, default=1)
        parser.add_argument("delay", type=int, default=0, nargs="?")
        parser.add_argument("-c", "--card", action="store_true")
        args = parser.parse_args(content.split())

        if args.delay > 0:
            sleep(args.delay)

        data = current_app.lipsum.get(args.lines)

        text = "\n\t".join(data)
        if args.card:
            card = lipsum_card(text)
            MessageHelper.reply_card(g.event.event.message.message_id, card)
        else:
            MessageHelper.reply_text(g.event.event.message.message_id, text)


class CommandMessageImpl:
    """
    If message starts with "/", we will consider as a "command", and use this class to handle it.
    """

    def __init__(self, **kwargs):
        self.parser = ArgumentParser()
        self.parser.add_argument("command", type=str)

        self.command_handler = {}

        # We can make several alias for each command
        register(self.command_handler, self.handle_command_get, ["/get", "/random"])

    def do(self):
        message_content = g.event.event.message.content
        message_at_list = [u.key for u in g.event.event.message.mentions] if g.event.event.message.mentions else []

        content = text_without_at_user(message_content["text"], message_at_list)

        # Split text into "command_name" and "parameters"
        name, param = self.parser.parse_known_args(content.strip().split())
        self.command_handler.get(name.command.lower(), self._idle)(param)

    def _idle(self, params: List[str]):
        MessageHelper.reply_text(g.event.event.message.message_id, "Command invalid")

    def handle_command_get(self, params: List[str]):
        parser = ArgumentParser()
        parser.add_argument(f"lines", type=int, nargs="?", default=1)
        parser.add_argument(f"delay", type=int, nargs="?", default=0)
        parser.add_argument(f"--card", action="store_true")
        args, _ = parser.parse_known_args(params)

        if args.delay > 0:
            sleep(args.delay)

        data = current_app.lipsum.get(args.lines)
        text = "\n\t".join(data)
        if args.card:
            card = lipsum_card(text)
            MessageHelper.reply_card(g.event.event.message.message_id, card)
        else:
            MessageHelper.reply_text(g.event.event.message.message_id, text)
