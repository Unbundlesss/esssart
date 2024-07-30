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
    def wrapper(self, param=None, *args, **kwargs):
        """When using this decorators, the signature should always be
        methodname(self, param=None, **kwargs)
        inside the function kwargs will be a dict and args will not be used"""

        lena = len(args)
        lenk = len(kwargs)
        # possibilities:
        # param, dict
        # args length = 1
        # param, kwargs
        # args = 0, kwargs > 0, param not None
        # no param, dict
        # args length = 0 and kwargs length = 0 and param is qdict
        # no param, kwargs
        # args length = 0 and kwargs length > 0 and param is None
        oparam = None

        if lena == 1 and isinstance(args[0], dict):
            qdict = args[0]
            oparam = param
        if lena == 0 and lenk > 0 and param is not None:
            qdict = kwargs
            oparam = param
        elif lena == 0 and lenk == 0 and param is not None:
            qdict = param
            oparam = None
        elif lena == 0 and lenk > 0 and param is None:
            qdict = kwargs
            oparam = None

        if not qdict:
            raise ValueError(f"{self.table}::{func.__name__} Missing object stuff")

        qlist = list(qdict.keys())

        if oparam:
            qlist += [oparam]

        if not self.whitelist(qlist):
            raise ValueError(f"{self.table}::{func.__name__} Invalid key in qdict")

        return func(self, oparam, **qdict)

    return wrapper
