from rusty_types.either import Either, _EitherMeta
from rusty_types.base import _BasePositional, _OrderedMultiType, _Uninstantiable


class Some(_BasePositional):
    def is_some(self) -> bool:
        return True

    def is_nothing(self) -> bool:
        return False


class _Nothing(_BasePositional):
    def is_some(self) -> bool:
        return False

    def is_nothing(self) -> bool:
        return True

    def unwrap(self):
        raise ValueError("Called unwrap() on a Nothing value")


Nothing = _Nothing()


class _OptionMeta(_EitherMeta):
    __left_class__ = Some
    __right_class__ = _Nothing

    def __getitem__(self, parameter):
        if isinstance(parameter, tuple) and len(parameter) > 1:
            raise TypeError("{} must be constructed as {}[{}_type]".format(self.__name__,
                                                                           self.__name__,
                                                                           self.__left_class__.__name__))

        return self.__class__(self.__name__, self.__bases__, dict(self.__dict__), (parameter, type(None)))


class Option(Either, metaclass=_OptionMeta):
    pass
