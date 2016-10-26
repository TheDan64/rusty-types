# from typing import Any, Dict, List


class _Uninstantiable:
    """ This base class is for any class that should not be instantiated the normal way

    """
    def __new__(self, *args, **kwargs):
        name = self.__class__

        if isinstance(self, type):
            name = self.__name__

        raise TypeError("Cannot instantiate %r" % name)


class _BaseMeta(type):
    """ A representative container for tagged union variants.

    It will eventually contain a more generic version of either.py's code.

    """
    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self):
        return "{}.{}".format(self.__module__, self.__name__)


class _BasePositional:
    """ A variant which may be associated with a value

    """
    def __init__(self, value=None):
        self._value = value

    def __repr__(self):
        r = "{}.{}".format(self.__module__, self.__class__.__name__)

        try:
            r += "({})".format(self.unwrap())
        except ValueError:
            pass

        return r

    def unwrap(self):
        return self._value


class _OrderedMultiTypeMeta(type):
    def __new__(cls, name, bases, namespace, parameters=None):
        if parameters is None:
            return super().__new__(cls, name, bases, namespace)

        self = super().__new__(cls, name, bases, {})

        # TODO: The following three steps can probably be
        # condensed or cleaned up somehow. Try/catch for
        # a tuple of types. Then validating all values are
        # types and finally parsing more sub tuple of types

        try:
            self._types, = parameters
        except ValueError:
            self._types = parameters

        for t in self._types:
            if not isinstance(t, (type, tuple)):
                raise TypeError("Parameters to generic types must be types. Found a {}".format(t))

        self._types = tuple(_OrderedMultiType[t] if isinstance(t, tuple) else t for t in self._types)

        return self

    def __init__(self, *args, **kwargs):
        pass

    def __instancecheck__(self, obj) -> bool:
        if isinstance(obj, tuple) and len(obj) == len(self._types):
            return all(isinstance(value, self._types[i]) for i, value in enumerate(obj))
        return False

    def __getitem__(self, parameters):
        return self.__class__(self.__name__, self.__bases__, dict(self.__dict__), parameters)


class _OrderedMultiType(_Uninstantiable, metaclass=_OrderedMultiTypeMeta):
    """ Tuple type definition.

    If you have a tuple with an int and a float (1, 1.1)
    then the typing module would have you use the Tuple
    construct to define its types:
    >>> from typing import Tuple
    >>> Tuple[int, float]

    But there are two major limitations here.
    1) The typings module is only available in 3.5+
    2) For some reason the Tuple class doesnt' support
        isinstance, making it practically useless for the
        point of this library

    Args:
        parameter: A tuple of types.

    Example:
        >>> tup_type = _OrderedMultiType[(int, float)]
        >>> assert isinstance((1, 1.1), tup_type)
    """
    pass
