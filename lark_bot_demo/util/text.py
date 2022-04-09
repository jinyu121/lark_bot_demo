import re
from typing import List

USER_PATTERN = re.compile(r"(@_user_(\d+)) ")


def text_without_at_user(text: str, users: List[str] = None) -> str:
    # Actually, we can not know exactly which part is "at user".
    # For example: the text is "@_user_1 Hello @_user_1 @_user_2 ",
    # and the users list is ["@_user_1", "@_user_2"], we can not know
    # which @_user_1 is fake.

    if not users:
        users = []
        counter = 0
        for u, n in USER_PATTERN.findall(text):
            if n == str(counter):
                users.append(u)
                counter += 1
    for user in users:
        text = text.replace(user + " ", " ", 1)

    return text.strip()
