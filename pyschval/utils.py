from __future__ import annotations

from typing import Iterator


def partition[T](data: list[T], size: int) -> Iterator[list[T]]:
    """Partition a list into chunks of size `size`.

    Args:
        data (list): The list to partition.
        size (int): The size of each chunk.

    Yields:
        Iterator[list]: The list of chunks.

    Raises:
        ValueError: If `size` is less than or equal to zero.
    """
    for i in range(0, len(data), size):
        yield data[i : i + size]
