from typing import Any

from defs import *


def warn(message: str, *parameters: Any) -> None:
    print("[warning] {}".format(message.format(*parameters)))


def repeated_registration(registration_type: str, type_id: int) -> None:
    warn("repeated {} registration for type {}", registration_type, type_id)


def missing_registration(registration_type: str, type_id: int) -> None:
    warn("missing {} registration for type {}", registration_type, type_id)


def unregistering_unregistered_creep(creep_name: str, target_type: int, details: str) -> None:
    warn("unregistering creep {} for {} which it is not registered for ({})", creep_name, target_type, details)


def unknown_type(type_of_type: str, type_id: int) -> None:
    warn("unknown {} type id {}", type_of_type, type_id)


_error_codes = {
    ERR_NOT_OWNER: "ERR_NOT_OWNER",
    ERR_NO_PATH: "ERR_NO_PATH",
    ERR_NAME_EXISTS: "ERR_NAME_EXISTS",
    ERR_BUSY: "ERR_BUSY",
    ERR_NOT_FOUND: "ERR_NOT_FOUND",
    ERR_NOT_ENOUGH_RESOURCES: "ERR_NOT_ENOUGH_RESOURCES",
    ERR_INVALID_TARGET: "ERR_INVALID_TARGET",
    ERR_FULL: "ERR_FULL",
    ERR_NOT_IN_RANGE: "ERR_NOT_IN_RANGE",
    ERR_INVALID_ARGS: "ERR_INVALID_ARGS",
    ERR_TIRED: "ERR_TIRED",
    ERR_NO_BODYPART: "ERR_NO_BODYPART",
    ERR_NOT_ENOUGH_EXTENSIONS: "ERR_NOT_ENOUGH_EXTENSIONS",
    ERR_RCL_NOT_ENOUGH: "ERR_RCL_NOT_ENOUGH",
    ERR_GCL_NOT_ENOUGH: "ERR_GCL_NOT_ENOUGH",
}


def transform_error_code(error_code: int) -> str:
    if error_code in _error_codes:
        return _error_codes[error_code]
    else:
        return "<error {}>".format(error_code)
