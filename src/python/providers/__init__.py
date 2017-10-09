from providers import cpucheck, exp_memory, targets


def instantiate() -> None:
    exp_memory.instantiate()
    cpucheck.instantiate()
    targets.instantiate()
