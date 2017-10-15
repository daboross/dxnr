from behaviors import spawn_fill, upgrade
from providers import registry


def register() -> None:
    registry.register(upgrade.exports)
    registry.register(spawn_fill.exports)
