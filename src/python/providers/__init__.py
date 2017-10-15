from providers import cpucheck, exp_memory, movement, targets


def apply_prototypes() -> None:
    movement.apply_prototypes()


def instantiate() -> None:
    exp_memory.instantiate()
    cpucheck.instantiate()  # depends on exp_memory
    targets.instantiate()  # depends on exp_memory
    movement.instantiate()
