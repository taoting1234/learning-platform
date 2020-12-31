import pytest

from app.libs.parser import Parser


def test_parser():
    parser = Parser("123", type_=int)
    with pytest.raises(Exception):
        parser.check("xxxx")
    parser = Parser("123", type_=int, required=True)
    with pytest.raises(Exception):
        parser.check(None)
    parser = Parser("123", type_=int, range_=(0, 10))
    with pytest.raises(Exception):
        parser.check(-1)
        parser.check(11)
    parser = Parser("123", type_=int, enum=[0, 1])
    with pytest.raises(Exception):
        parser.check(-1)
        parser.check(2)
