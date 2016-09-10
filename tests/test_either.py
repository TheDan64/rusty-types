from rusty_types.either import Either, Left, Right

import pytest
import sys


def test_uninstantiable():
    with pytest.raises(TypeError):
        Either()


def test_left():
    either = Either[int, str]

    assert isinstance(Left(1), either)
    assert not isinstance(Left("foo"), either)

    either = Either[None, str]

    assert isinstance(Left(), either)


def test_right():
    either = Either[int, str]

    assert isinstance(Right("foo"), either)
    assert not isinstance(Right(1), either)

    either = Either[int, None]

    assert isinstance(Right(), either)


def test_typehint_support():
    def foo(either: Either[int, str]) -> Either[str, int]:
        return Left("foo") if either.is_right() else Right(1)


@pytest.mark.skipif(sys.version_info < (3, 5), reason="Typing available in Py3.5+ only")
def test_typing_support():
    from typing import Dict, List

    either = Either[None, List[Dict[str, str]]]

    assert isinstance(Right([{"foo": "bar"}]), either)
    assert not isinstance(Right({"foo": "bar"}), either)

    assert not isinstance(Right([{"foo": None}]), either)
    assert not isinstance(Right([{1: "bar"}]), either)
