from meta.registry import Database
from meta.registry_exports import Exports

_registry = Database()


def get() -> Database:
    return _registry


def register(exports: Exports) -> None:
    _registry.register(exports)


def finalize() -> None:
    _registry.finalize()
