from typing import Generic, TypeVar, Union

L = TypeVar('L')
R = TypeVar('R')


class Left(Generic[L]):
    def __init__(self, value: L) -> None:
        self._value = value

    def is_left(self) -> bool:
        return True

    def is_right(self) -> bool:
        return False

    def unwrap(self) -> L:
        return self._value


class Right(Generic[R]):
    def __init__(self, value: R) -> None:
        self._value = value

    def is_left(self) -> bool:
        return False

    def is_right(self) -> bool:
        return True

    def unwrap(self) -> R:
        return self._value


Either = Union[Left[L], Right[R]]
