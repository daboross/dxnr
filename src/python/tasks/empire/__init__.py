from providers import registry
from tasks.empire import creep_memory_clean, visualize_passing_movement


def register() -> None:
    registry.register(visualize_passing_movement.exports)
    registry.register(creep_memory_clean.exports)
