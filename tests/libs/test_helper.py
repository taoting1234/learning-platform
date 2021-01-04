import pytest

from app.libs.helper import change_columns


def test_change_columns():
    with pytest.raises(Exception):
        change_columns("i")
    assert sorted(change_columns("1-3,   1 0,15-13,11-11")) == sorted(
        [1, 2, 3, 10, 13, 14, 15, 11]
    )
