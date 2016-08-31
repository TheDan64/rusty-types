#! /usr/bin/env python3

from typing import Any, Dict, List


class Uninstantiable:
    def __new__(self, *args, **kwargs):
        raise TypeError("Cannot instantiate %r" % self.__class__)


class BaseMeta(type):
    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self):
        return "{}.{}".format(self.__module__, getattr(self, "__qualname__", self.__name__))


class EitherMeta(BaseMeta):
    pass


class ResultMeta(EitherMeta):
    # TODO: Turn this into Either, and derive as Result
    def __new__(cls, name, bases, namespace, parameters=None):
        if parameters is None:
            return super().__new__(cls, name, bases, namespace)

        if not isinstance(parameters, tuple):
            raise TypeError("A Result must be constructed as Result[ok_type, err_type]")

        ok_type, err_type = parameters
        # TODO: Set None to type(None)

        self = super().__new__(cls, name, bases, {})
        self.__ok_type__ = ok_type
        self.__err_type__ = err_type

        return self

    def __instancecheck__(self, obj):
        if not self.__ok_type__ or not self.__err_type__:
            return False

        if isinstance(obj, Ok):
            return isinstance(obj.value, self.__ok_type__)
        if isinstance(obj, Err):
            return isinstance(obj.value, self.__err_type__)

        # Raise NotImplemented?
        raise TypeError("Result cannot be used with isinstance().")

    def __subclasscheck__(self, cls):
        if cls is Any:
            return True

    def __getitem__(self, parameters):
        if not isinstance(parameters, tuple) or len(parameters) != 2:
            raise TypeError("A Result must be constructed as Result[ok_type, err_type]")

        return self.__class__(self.__name__, self.__bases__, dict(self.__dict__), parameters)

    def __repr__(self):
        r = super().__repr__()

        if self.__ok_type__ and self.__err_type__:
            r += "[{}, {}]".format(self.__ok_type__.__name__, self.__err_type__.__name__)

        return r


class Result(Uninstantiable, metaclass=ResultMeta):
    __ok_type__ = None
    __err_type__ = None


class Ok:
    def __init__(self, value=None):
        self._value = value

    def is_ok(self):
        return True

    def is_err(self):
        return False

    @property
    def value(self):
        return self._value


class Err:
    def __init__(self, value=None):
        self._value = value

    def is_ok(self):
        return False

    def is_err(self):
        return True

    @property
    def value(self):
        return self._value

print(Result)
print(Result[int, str], type(Result[int, str]))
print(isinstance(Ok(1), Result[int, str]))
print(not isinstance(Ok("asd"), Result[int, str]))
print(isinstance(Err("asd"), Result[int, str]))
print(not isinstance(Err(1), Result[int, str]))
print(not isinstance(Ok(1), Result))
print(isinstance(Ok(), Result[None, List[Dict[str, Any]]]))
print(isinstance(Err([{"foo": "bar"}]), Result[None, List[Dict[str, Any]]]))
