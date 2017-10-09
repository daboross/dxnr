from providers import registry
from tasks.empire import creep_memory_clean


def register() -> None:
    registry.register(creep_memory_clean.exports)
