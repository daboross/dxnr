from typing import Any, Callable, Optional, TypeVar

from defs import *


def error(err: Any, message: str) -> None:
    if err == undefined:
        if err is None:
            error_description = "null error"
        else:
            error_description = "undefined error"
    else:
        if err.stack == undefined:
            error_description = "error {} with stack: undefined".format(err)
        else:
            error_description = "error {} with stack:\n{}".format(err, err.stack)

    full_message = "[error] {}: {}".format(message, error_description)
    print(full_message)
    Game.notify(full_message)


_O = TypeVar('_O')


def execute_catching(the_function: Callable[..., _O], error_description: Callable[..., str], *args: Any) \
        -> Optional[_O]:
    result = None
    # noinspection PyBroadException
    try:
        result = the_function(*args)
    except:
        caught = __except0__
        error(caught, error_description(*args))
    return result


def catching(error_description: Callable[..., str], default_value: _O = None) \
        -> Callable[[Callable[..., _O]], Callable[..., _O]]:
    def wrap(thing: Callable[..., _O]) -> Callable[..., _O]:
        def new_definition(*args: Any) -> _O:
            result = default_value
            # noinspection PyBroadException
            try:
                result = thing(*args)
            except:
                caught = __except0__
                error(caught, error_description(*args))
            return result

        return new_definition

    return wrap
