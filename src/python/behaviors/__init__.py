from behaviors import upgrade
from providers import registry


def register():
    registry.register(upgrade.exports)
