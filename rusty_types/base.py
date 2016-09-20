from typing import Any, Dict, List


class _Uninstantiable:
    def __new__(self, *args, **kwargs):
        raise TypeError("Cannot instantiate %r" % self.__class__)


class _BaseMeta(type):
    """ Metaclass for every type defined here.

    """
    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self):
        return "{}.{}".format(self.__module__, self.qualname)

    @property
    def qualname(self):
        return getattr(self, "__qualname__", self.__name__)

    def __subclasscheck__(self, cls):  # FIXME
        if cls is Any:
            return True


class _BasePositional:
    def __init__(self, value=None):
        self._value = value

    @property
    def value(self):
        return self._value

    @property
    def qualname(self):
        return getattr(self, "__qualname__", self.__name__)
