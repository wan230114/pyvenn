from functools import wraps


def validate_arguments():
    def outer(function):
        @wraps(function)
        def inner(*args, **kwargs):
            print(args)
            print(kwargs)
            return function(*args, **kwargs)
        return inner
    return outer
