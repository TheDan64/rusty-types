from typing import ClassVar, Generic, TypeVar, Union

O = TypeVar('O')
E = TypeVar('E')


class Ok(Generic[O]):
    def __init__(self, value: O) -> None:
        self._value = value

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def unwrap(self) -> O:
        return self._value


class Err(Generic[E]):
    def __init__(self, value: E) -> None:
        self._value = value

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def unwrap(self) -> E:
        return self._value

Result = Union[Ok[O], Err[E]]
