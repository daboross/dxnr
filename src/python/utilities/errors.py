from typing import Any, Callable, Optional, TypeVar

from defs import *


def error(err: Any, message: str):
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


__pragma__('skip')
_I = TypeVar('_I')
_O = TypeVar('_O')
__pragma__('noskip')


def execute_catching(the_function: Callable[_I, _O], error_description: Callable[_I, str], *args: _I) \
        -> Optional[_O]:
    result = None
    # noinspection PyBroadException
    try:
        result = the_function(*args)
    except:
        caught = __except0__
        error(caught, error_description(*args))
    return result


def catching(error_description: Callable[_I, str], default_value=None) \
        -> Callable[[Callable[_I, _O]], Callable[_I, _O]]:
    def wrap(thing):
        def new_definition(*args):
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
