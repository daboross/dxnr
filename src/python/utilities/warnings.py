from typing import Any


def warn(message: str, *parameters: Any) -> None:
    print("[warning] {}".format(message.format(*parameters)))


def repeated_registration(registration_type: str, type_id: int) -> None:
    warn("repeated {} registration for type {}", registration_type, type_id)


def missing_registration(registration_type: str, type_id: int) -> None:
    warn("missing {} registration for type {}", registration_type, type_id)


def unregistering_unregistered_creep(creep_name: str, target_type: int) -> None:
    warn("unregistering creep {} for {} which it is not registered for", creep_name, target_type)
