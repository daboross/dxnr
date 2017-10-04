from defs import *

_limit = 100


def instantiate():
    global _limit
    if Game.cpu.tickLimit >= 500:
        _limit = 400
    else:
        _limit = max(
            Game.cpu.limit,
            Game.cpu.tickLimit - 150,
            int((Game.cpu.limit + Game.cpu.tickLimit) / 2)
        )

def is_over_limit():
    return Game.cpu.getUsed() > _limit