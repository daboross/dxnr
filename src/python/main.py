from defs import *


def main():
    """
    Main game logic loop shim.
    """
    from providers import cpucheck

    cpucheck.instantiate()

    if cpucheck.is_over_limit():
        return

    import logic
    logic.main()


module.exports.loop = main
