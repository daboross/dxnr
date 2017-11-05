from typing import Optional

from core.kernel import Kernel

_kernel = None


def instantiate() -> None:
    global _kernel
    _kernel = None


def store_kernel(kernel: Kernel) -> None:
    global _kernel
    _kernel = kernel


def get_kernel() -> Optional[Kernel]:
    return _kernel
