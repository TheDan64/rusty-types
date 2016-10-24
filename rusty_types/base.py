# from typing import Any, Dict, List


class _Uninstantiable:
    def __new__(self, *args, **kwargs):
        name = self.__class__

        if isinstance(self, type):
            name = self.__name__

        raise TypeError("Cannot instantiate %r" % name)


class _BaseMeta(type):
    """ Metaclass for every type defined here.

    """
    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self):
        return "{}.{}".format(self.__module__, self.__name__)


class _BasePositional:
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
