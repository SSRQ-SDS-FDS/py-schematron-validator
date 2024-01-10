import pytest

from pyschval.utils import partition


@pytest.mark.parametrize(
    "data, size, expected",
    [
        ([1, 2, 3, 4, 5, 6], 2, [[1, 2], [3, 4], [5, 6]]),
        (["a", "b", "c", "d", "e", "f"], 3, [["a", "b", "c"], ["d", "e", "f"]]),
        ([], 1, []),
        ([1, 2, 3], 5, [[1, 2, 3]]),
    ],
)
def test_partition(data: list[int], size: int, expected: list[list[int]]):
    result = list(partition(data, size))
    assert result == expected


def test_partition_error():
    data = [1, 2, 3]
    size = 0
    with pytest.raises(ValueError):
        list(partition(data, size))
