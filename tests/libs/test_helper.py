import pytest

from app.libs.helper import change_columns
from app.libs.parser import Parser


def test_parser():
    parser = Parser(name="123", type_=int, required=True, description="")
    with pytest.raises(Exception):
        parser.check("xxxx")
    parser = Parser(name="123", type_=int, required=True, description="")
    with pytest.raises(Exception):
        parser.check(None)
    parser = Parser(name="123", type_=int, required=True, description="", range_=(0, 10))
    with pytest.raises(Exception):
        parser.check(-1)
    with pytest.raises(Exception):
        parser.check(11)
    parser = Parser(name="123", type_=int, required=True, description="", enum=[0, 1])
    with pytest.raises(Exception):
        parser.check(-1)
    with pytest.raises(Exception):
        parser.check(2)


def test_change_columns():
    with pytest.raises(Exception):
        change_columns("i")
    assert sorted(change_columns("1:3,,   1 0,15:13,11:11, -2:-1")) == sorted([1, 2, 3, 10, 13, 14, 15, 11, -1, -2])
