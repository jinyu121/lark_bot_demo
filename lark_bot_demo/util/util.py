import logging
from typing import List, Union


def register(dic, fn, alias: Union[str, List[str]]):
    if isinstance(alias, str):
        alias = [alias]
    for name in alias:
        name = name.lower()
        if name not in dic.keys():
            dic[name] = fn
        else:
            logging.warning(f"Alias `{name}` have been band to {dic[name]}, pass")
