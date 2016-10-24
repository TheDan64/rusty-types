from rusty_types.result import Result, Ok, Err

import pytest
import sys


def test_uninstantiable():
    with pytest.raises(TypeError):
        Result()


def test_ok():
    result = Result[int, str]

    assert isinstance(Ok(1), result)
    assert not isinstance(Ok("foo"), result)

    result = Result[None, str]

    assert isinstance(Ok(), result)
    assert Ok(1).is_ok()
    assert not Ok(1).is_err()
    assert Ok(1).unwrap() == 1


def test_err():
    result = Result[int, str]

    assert isinstance(Err("foo"), result)
    assert not isinstance(Err(1), result)

    result = Result[int, None]

    assert isinstance(Err(), result)
    assert Err(1).is_err()
    assert not Err(1).is_ok()
    assert Err(1).unwrap() == 1


def test_invalid_parameters():
    with pytest.raises(TypeError):
        Result[int]

    with pytest.raises(TypeError):
        Result[int, str, int]


def test_typehint_support():
    def foo(result: Result[int, str]) -> Result[str, int]:
        return Ok("foo") if result.is_err() else Err(1)


@pytest.mark.skipif(sys.version_info < (3, 5), reason="Typing available in Py3.5+ only")
def test_typing_support():
    from typing import Dict, List

    result = Result[None, List[Dict[str, str]]]

    assert isinstance(Err([{"foo": "bar"}]), result)
    assert not isinstance(Err({"foo": "bar"}), result)
    assert not isinstance(1, result)

    # REVIEW: Doesn't seem supported by type hints?
    # assert not isinstance(Err([{"foo": None}]), result)
    # assert not isinstance(Err([{1: "bar"}]), result)
