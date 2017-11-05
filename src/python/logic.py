import processes
import providers
from core.kernel import Kernel
from defs import *
from providers import registry
from utilities import errors

#registry.register(tasks.exports)
registry.register(processes.exports)

providers.apply_prototypes()


@errors.catching(lambda: "running main")
def main() -> None:
    """
    Main game logic loop.
    """

    providers.instantiate()

    kernel = Kernel()

    kernel.instantiate_processes()

    kernel.run()


module.exports.loop = main
