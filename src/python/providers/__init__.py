from providers import targets, cpucheck


def instantiate() -> None:
    cpucheck.instantiate()
    targets.instantiate()
