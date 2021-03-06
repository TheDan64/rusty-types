from rusty_types.option import Option, Some, Nothing

import pytest
import sys


def test_uninstantiable():
    with pytest.raises(TypeError):
        Option()

    with pytest.raises(TypeError):
        Nothing()


def test_some():
    option = Option[int]

    assert isinstance(Some(1), option)
    assert not isinstance(Some("foo"), option)

    option = Option[None]

    assert isinstance(Some(), option)
    assert Some(1).is_some()
    assert not Some(1).is_nothing()
    assert Some(1).unwrap() == 1


def test_nothing():
    option = Option[int]

    assert isinstance(Nothing, option)

    option = Option[int]

    assert Nothing.is_nothing()
    assert not Nothing.is_some()

    with pytest.raises(ValueError):
        Nothing.unwrap()


def test_invalid_parameters():
    with pytest.raises(TypeError):
        Option[int, str]

    with pytest.raises(TypeError):
        Option[(int, float), str]

    with pytest.raises(TypeError):
        Option[1]

    with pytest.raises(TypeError):
        Option[1,]


def test_tuple():
    option = Option[(int, float),]

    assert isinstance(Some((1, 1.1)), option)
    assert not isinstance(Some((1, "str")), option)

    option = Option[(int, (float, str)),]

    assert isinstance(Some((1, (1.1, "foo"))), option)

    option = Option[(int, (float, (str, list))),]

    assert isinstance(Some((1, (1.1, ("foo", [1, 2])))), option)


def test_typehint_support():
    def foo(option: Option[int]) -> Option[str]:
        return Some("foo") if option.is_nothing() else Nothing


@pytest.mark.skipif(sys.version_info < (3, 5), reason="Typing available in Py3.5+ only")
def test_typing_support():
    from typing import Dict, List

    option = Option[List[Dict[str, str]]]

    assert isinstance(Some([{"foo": "bar"}]), option)
    assert isinstance(Nothing, option)
    assert not isinstance(1, option)
