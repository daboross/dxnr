from providers import cpucheck, targets


def instantiate() -> None:
    cpucheck.instantiate()
    targets.instantiate()
