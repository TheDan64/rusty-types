#! /usr/bin/env python3

from typing import Any, Dict, List


class Uninstantiable:
    def __new__(self, *args, **kwargs):
        raise TypeError("Cannot instantiate %r" % self.__class__)


class BaseMeta(type):
    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self):
        return "{}.{}".format(self.__module__, self.qualname)

    @property
    def qualname(self):
        return getattr(self, "__qualname__", self.__name__)


class EitherMeta(BaseMeta):
    __left_name__ = "__left_type__"
    __right_name__ = "__right_type__"

    def __new__(cls, name, bases, namespace, parameters=None):
        if parameters is None:
            return super().__new__(cls, name, bases, namespace)

        if not isinstance(parameters, tuple):
            raise TypeError("A {} must be constructed as {}[left_type, right_type]".format(cls.qualname, cls.qualname))

        left_type, right_type = parameters
        # TODO: Set None to type(None)

        self = super().__new__(cls, name, bases, {})

        setattr(self, cls.__left_name__, left_type)
        setattr(self, cls.__right_name__, right_type)

        return self

    def __repr__(self):
        r = super().__repr__()

        if self.__left_type__ and self.__right_type__:
            r += "[{}, {}]".format(self.__left_type__.__name__, self.__right_type__.__name__)

        return r


class Either(Uninstantiable, metaclass=EitherMeta):
    __left_type__ = None
    __right_type__ = None


class Left:
    def __init__(self, value=None):
        self._value = value

    def is_left(self):
        return True

    def is_right(self):
        return False

    @property
    def value(self):
        return self._value


class Right:
    def __init__(self, value=None):
        self._value = value

    def is_left(self):
        return False

    def is_right(self):
        return True

    @property
    def value(self):
        return self._value


class ResultMeta(EitherMeta):
    __left_name__ = "__ok_type__"
    __right_name__ = "__err_type__"

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
        r = super(EitherMeta, self).__repr__()

        if self.__ok_type__ and self.__err_type__:
            r += "[{}, {}]".format(self.__ok_type__.__name__, self.__err_type__.__name__)

        return r


class Result(Uninstantiable, metaclass=ResultMeta):
    __ok_type__ = None
    __err_type__ = None


class Ok(Left):
    def is_ok(self):
        return True

    def is_err(self):
        return False


class Err(Right):
    def is_ok(self):
        return False

    def is_err(self):
        return True

print(Result)
print(Result[int, str], type(Result[int, str]))
print(isinstance(Ok(1), Result[int, str]))
print(not isinstance(Ok("asd"), Result[int, str]))
print(isinstance(Err("asd"), Result[int, str]))
print(not isinstance(Err(1), Result[int, str]))
print(not isinstance(Ok(1), Result))
print(isinstance(Ok(), Result[None, List[Dict[str, Any]]]))
print(isinstance(Err([{"foo": "bar"}]), Result[None, List[Dict[str, Any]]]))
