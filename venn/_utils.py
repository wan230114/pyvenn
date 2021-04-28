from functools import wraps
from warnings import warn


KEYWORD_ARGS_ERROR = ("Starting from version 0.1.4, {}() only accepts `data` "
    "as a positional argument; remaining arguments must be passed "
    "as keyword arguments (e.g., cmap='Greens')")

DEPRECATED_ARG_ERROR = "Argument `{}` is deprecated and will have no effect"


warn_deprecation = lambda message: warn(message, FutureWarning)


def validate_arguments():
    def outer(function):
        @wraps(function)
        def inner(*args, **kwargs):
            if len(args) > 1:
                raise TypeError(KEYWORD_ARGS_ERROR.format(function.__name__))
            if "figsize" in kwargs:
                warn_deprecation(DEPRECATED_ARG_ERROR.format("figsize"))
                del kwargs["figsize"]
            return function(*args, **kwargs)
        return inner
    return outer
