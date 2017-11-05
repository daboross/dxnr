import processes
import providers
from core.kernel import Kernel
from defs import *
from providers import global_kernel_handle, registry
from providers.interface import RootInterface
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

    global_kernel_handle.store_kernel(kernel)


module.exports.loop = main

js_global.i = RootInterface()
