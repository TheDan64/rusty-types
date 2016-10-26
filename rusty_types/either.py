from rusty_types.base import _BaseMeta, _BasePositional, _OrderedMultiType, _Uninstantiable


class Left(_BasePositional):
    def is_left(self) -> bool:
        return True

    def is_right(self) -> bool:
        return False


class Right(_BasePositional):
    def is_left(self) -> bool:
        return False

    def is_right(self) -> bool:
        return True


class _EitherMeta(_BaseMeta):
    __left_class__ = Left
    __right_class__ = Right

    def __new__(cls, name, bases, namespace, parameters=None):
        if parameters is None:
            return super().__new__(cls, name, bases, namespace)

        if not isinstance(parameters, tuple):
            raise TypeError("A {} must be constructed as {}[{}_type, {}_type]".format(cls.__qualname__,
                                                                                      cls.__qualname__,
                                                                                      cls.__left_class__.__qualname__,
                                                                                      cls.__right_class__.__qualname__))
        left_type, right_type = parameters

        if left_type is None:
            left_type = type(None)

        if right_type is None:
            right_type = type(None)

        if isinstance(left_type, tuple):
            left_type = _OrderedMultiType[left_type]

        if isinstance(right_type, tuple):
            right_type = _OrderedMultiType[right_type]

        if not isinstance(left_type, type):
            raise TypeError("Type parameters must be types. Found a {}".format(left_type))

        if not isinstance(right_type, type):
            raise TypeError("Type parameters must be types. Found a {}".format(right_type))

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

    def __instancecheck__(self, obj) -> bool:
        # REVIEW: Is this check needed?
        if not self.__left_type__ or not self.__right_type__:
            return False

        if isinstance(obj, self.__left_class__):
            return isinstance(obj._value, self.__left_type__)

        if isinstance(obj, self.__right_class__):
            return isinstance(obj._value, self.__right_type__)

        return False

    def __getitem__(self, parameters):
        if not isinstance(parameters, tuple) or len(parameters) != 2:
            raise TypeError("{} must be constructed as {}[{}_type, {}_type]".format(self.__name__,
                                                                                    self.__name__,
                                                                                    self.__left_class__.__name__,
                                                                                    self.__right_class__.__name__))

        return self.__class__(self.__name__, self.__bases__, dict(self.__dict__), parameters)


class Either(_Uninstantiable, metaclass=_EitherMeta):
    __left_type__ = None
    __right_type__ = None
