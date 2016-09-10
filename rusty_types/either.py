from rusty_types.base import _BaseMeta, _BasePositional, _Uninstantiable


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
