# Lark Bot Demo

This repo demonstrates how to create a LarkBot with a simple chatbot.

In this demo, you can see how to:

- use the official `larksuite-oapi` package
- use thread to process the message to meet 1s(for message) / 3s(for card) timeout limit
- use card, and interaction of card

## Functions of this bot:

### Normal text message

- Input: `N`
    - output: N paragraphs of Lipsum
- Input `N M`
    - output: N paragraphs of Lipsum, after M seconds
- Input `N M --card`
    - output: N paragraphs of Lipsum, after M seconds, using card

### Command mode

Normal text mode and command mode are two different modes.

Message starts with `/` will be considered as command.

In this demo, the following commands are available:

- Input: `/get N`
    - output: N paragraphs of Lipsum
- Input: `/get N M`
    - output: N paragraphs of Lipsum, after M seconds
- Input: `/get N M --card`
    - output: N paragraphs of Lipsum, after M seconds, using card

### Card

This repo demonstrates how to use card in sync and async mode.

Due to lack of async update API in Lark SDK, this demo does not support async update mode.