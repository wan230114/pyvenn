from functools import wraps
from warnings import warn


warn_deprecation = lambda message: warn(message, FutureWarning)

INVALID_DATA_ERROR = ("Argument `data` for `{}()` must be a dictionary (or a "
    "dictionary-like structure) of sets")
KEYWORD_ARGS_ERROR = ("Starting from version 0.1.4, `{}()` only accepts `data` "
    "as a positional argument; remaining arguments must be passed "
    "as keyword arguments (e.g., cmap='Greens')")
DEPRECATED_ARG_WARNING = "Argument `{}` is deprecated and will have no effect"


def is_valid_dataset_dict(data):
    """Validate passed data (must be dictionary of sets)"""
    if not (hasattr(data, "keys") and hasattr(data, "values")):
        return False
    for dataset in data.values():
        if not isinstance(dataset, set):
            return False
    else:
        return True


def validate_arguments():
    """Validate all passed positional and keyword arguments"""
    def outer(function):
        @wraps(function)
        def inner(*args, **kwargs):
            if len(args) and (not is_valid_dataset_dict(args[0])):
                raise TypeError(INVALID_DATA_ERROR.format(function.__name__))
            if len(args) > 1:
                raise TypeError(KEYWORD_ARGS_ERROR.format(function.__name__))
            if kwargs.get("figsize"):
                warn_deprecation(DEPRECATED_ARG_WARNING.format("figsize"))
            if "figsize" in kwargs:
                del kwargs["figsize"]
            if kwargs.get("petal_labels") and kwargs.get("fmt"):
                warn("Passing `fmt` with `petal_labels` will have no effect")
            return function(*args, **kwargs)
        return inner
    return outer
