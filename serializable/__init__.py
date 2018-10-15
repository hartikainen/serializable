import inspect
import sys


def parse_self_arg_key(spec, locals_, instance):
    self_arg_key = None

    if locals_[spec.args[0]] is instance:
        self_arg_key =  spec.args[0]

    if self_arg_key is None:
        if 'self' in spec.args and instance is locals_['self']:
            self_arg_key =  'self'

    if self_arg_key is None:
        possible_self_arg_keys = [
            arg_name for arg_name in spec.args
            if locals_[arg_name] is instance
        ]

        if len(possible_self_arg_keys) > 0:
            raise ValueError(
                "Unable to serialize and object when multiple local"
                " variables refer to self. Typically, 'self' should refer"
                " to the object itself, but found the following: {}"
                "".format(possible_self_arg_keys))

        self_arg_key = possible_self_arg_keys[0]

    return self_arg_key


class Serializable(object):

    def __init__(self, *args, **kwargs):
        self.__args = args
        self.__kwargs = kwargs

    def __initialize(self, locals_):
        if getattr(self, "__initialized", False):
            return

        spec = (inspect.getfullargspec(self.__init__)
                if sys.version_info >= (3, 0)
                else inspect.getargspec(self.__init__))

        self_arg_key = parse_self_arg_key(spec, locals_, self)

        if self_arg_key is None:
            raise NotImplementedError(
                "Unable to serialize object without 'self'.")

        args_values = tuple((
            locals_[arg_key]
            for arg_key in spec.args
            if arg_key != self_arg_key))

        varargs_values = locals_[spec.varargs] if spec.varargs else ()

        full_args_values = tuple(args_values) + tuple(varargs_values)

        varkw_values = (
            (locals_[spec.varkw] if spec.varkw else {})
            if sys.version_info >= (3, 0)
            else (locals_[spec.keywords] if spec.keywords else {}))

        kwonlyargs_values = {
            key: locals_[key]
            for key in spec.kwonlyargs
        }

        full_kwargs_values = varkw_values.copy()
        full_kwargs_values.update(kwonlyargs_values)

        self.__args = full_args_values
        self.__kwargs = full_kwargs_values
        self.__self_arg_key = self_arg_key

        self.__initialized = True

    def __getstate__(self):
        state = {
            '__args': self.__args,
            '__kwargs': self.__kwargs,
            '__self_arg_key': self.__self_arg_key,
        }

        return state

    def __setstate__(self, state):
        out = type(self)(*state["__args"], **state["__kwargs"])
        self.__dict__.update(out.__dict__)

    @classmethod
    def clone(cls, instance, **kwargs):
        assert isinstance(instance, Serializable) and instance.__initialized

        spec = (inspect.getfullargspec(instance.__init__)
                if sys.version_info >= (3, 0)
                else inspect.getargspec(instance.__init__))

        state = instance.__getstate__()

        in_order_arg_keys = [
            arg_key for arg_key in spec.args
            if arg_key != state['__self_arg_key']
        ]

        state["__args"] = tuple(state["__args"])
        for kw, val in kwargs.items():
            if kw in in_order_arg_keys:
                state["__args"][in_order_arg_keys.index(kw)] = val
            else:
                state["__kwargs"][kw] = val

        out = type(instance).__new__(type(instance))
        out.__setstate__(state)

        return out
