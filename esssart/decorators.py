import functools

def debug(func):
    """Print the function signature and return value"""

    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={repr(v)}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__}() returned {repr(value)}")
        return value

    return wrapper_debug


def handle_params(func):
    @functools.wraps(func)
    def wrapper(self, qdict):
        if not qdict:
            raise ValueError(f"{self.table}::{func.__name__} Missing object stuff")

        qlist = list(qdict.keys())

        if not self.whitelist(qlist):
            raise ValueError(f"{self.table}::{func.__name__} Invalid key in qdict")

        return func(self, qdict)

    return wrapper
