from typing import Any, Dict

from defs import *


def create_name_excluding_keys_to(existing: Dict[Any, Any]) -> str:
    name = _random_name()
    while name in existing:
        name += _random_name()
    return name


def _random_name() -> str:
    num = 40 + _.random(0, 85)
    if num > 91:
        num += 1  # skip 92
    return String.fromCodePoint(num)
