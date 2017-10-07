from behaviors import upgrade
from providers import registry


def register() -> None:
    registry.register(upgrade.exports)
