from rusty_types.either import Either, _EitherMeta
from rusty_types.base import _BasePositional


class Ok(_BasePositional):
    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False


class Err(_BasePositional):
    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True


class _ResultMeta(_EitherMeta):
    __left_class__ = Ok
    __right_class__ = Err


class Result(Either, metaclass=_ResultMeta):
    pass
