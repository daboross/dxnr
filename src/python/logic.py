import providers
import tasks
import trename_processes
from core.kernel import Kernel
from defs import *
from providers import registry
from utilities import errors

registry.register(tasks.exports)
registry.register(trename_processes.exports)
registry.finalize()

providers.apply_prototypes()


@errors.catching(lambda: "running main")
def main() -> None:
    """
    Main game logic loop.
    """

    providers.instantiate()

    kernel = Kernel()

    kernel.run()


module.exports.loop = main
