from providers import cpucheck, targets, exp_memory


def instantiate() -> None:
    exp_memory.instantiate()
    cpucheck.instantiate()
    targets.instantiate()
