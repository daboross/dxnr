from providers import targets, cpucheck


def instantiate():
    cpucheck.instantiate()
    targets.instantiate()
