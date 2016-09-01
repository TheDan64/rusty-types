#! /usr/bin/env python3

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


class _BasePositional:
    def __init__(self, value=None):
        self._value = value

    @property
    def value(self):
        return self._value

    @property
    def qualname(self):
        return getattr(self, "__qualname__", self.__name__)


class Left(_BasePositional):
    def is_left(self):
        return True

    def is_right(self):
        return False


class Right(_BasePositional):
    def is_left(self):
        return False

    def is_right(self):
        return True


class _EitherMeta(_BaseMeta):
    __left_class__ = Left
    __right_class__ = Right

    def __new__(cls, name, bases, namespace, parameters=None):
        if parameters is None:
            return super().__new__(cls, name, bases, namespace)

        if not isinstance(parameters, tuple):
            raise TypeError("A {} must be constructed as {}[{}_type, {}_type]".format(cls.qualname,
                                                                                      cls.qualname,
                                                                                      cls.__left_class__.qualname,
                                                                                      cls.__right_class__.qualname))

        left_type, right_type = parameters

        if left_type is None:
            left_type = type(None)

        if right_type is None:
            right_type = type(None)

        self = super().__new__(cls, name, bases, {})

        self.__left_type__ = left_type
        self.__right_type__ = right_type

        return self

    def __repr__(self):
        r = super().__repr__()

        if self.__left_type__ and self.__right_type__:
            r += "[{}, {}]".format(self.__left_type__.__name__,
                                   self.__right_type__.__name__)

        return r

    def __instancecheck__(self, obj):
        if not self.__left_type__ or not self.__right_type__:
            return False

        if isinstance(obj, self.__left_class__):
            return isinstance(obj.value, self.__left_type__)
        if isinstance(obj, self.__right_class__):
            return isinstance(obj.value, self.__right_type__)

        # Raise NotImplemented?
        raise TypeError("Result cannot be used with isinstance().")

    def __getitem__(self, parameters):
        if not isinstance(parameters, tuple) or len(parameters) != 2:
            # FIXME
            raise TypeError("A {} must be constructed as {}[{}_type, {}_type]".format(self.qualname,
                                                                                      self.qualname,
                                                                                      self.__left_class__.qualname,
                                                                                      self.__right_class__.qualname))

        return self.__class__(self.__name__, self.__bases__, dict(self.__dict__), parameters)


class Either(_Uninstantiable, metaclass=_EitherMeta):
    __left_type__ = None
    __right_type__ = None


class Ok(_BasePositional):
    def is_ok(self):
        return True

    def is_err(self):
        return False


class Err(_BasePositional):
    def is_ok(self):
        return False

    def is_err(self):
        return True


class _ResultMeta(_EitherMeta):
    __left_class__ = Ok
    __right_class__ = Err

    def __subclasscheck__(self, cls):
        if cls is Any:
            return True


class Result(Either, metaclass=_ResultMeta):
    pass


print(Result)
print(isinstance(Ok(1), Result[int, str]))
print(not isinstance(Ok("asd"), Result[int, str]))
print(isinstance(Err("asd"), Result[int, str]))
print(not isinstance(Err(1), Result[int, str]))
print(not isinstance(Ok(1), Result))
print(isinstance(Ok(), Result[None, List[Dict[str, Any]]]))
print(isinstance(Err([{"foo": "bar"}]), Result[None, List[Dict[str, Any]]]))
