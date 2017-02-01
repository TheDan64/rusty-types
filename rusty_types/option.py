from typing import Generic, TypeVar, Union

S = TypeVar('S')


class Some(Generic[S]):
    def __init__(self, value: S) -> None:
        self._value = value

    def is_some(self) -> bool:
        return True

    def is_nothing(self) -> bool:
        return False

    def unwrap(self) -> S:
        return self._value


class _Nothing:
    def __init__(self) -> None:
        self._value = None

    def is_some(self) -> bool:
        return False

    def is_nothing(self) -> bool:
        return True

    def unwrap(self) -> None:
        raise ValueError("Called unwrap() on a Nothing value")


Nothing = _Nothing()

Option = Union[Some[S], _Nothing]
