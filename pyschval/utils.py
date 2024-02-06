from pathlib import Path
from typing import Iterator, TypeVar

T = TypeVar("T")


def is_file_and_exists(file: str | Path) -> bool:
    """Check if `file` is a file and exists.

    Args:
        file (T): The file to check.

    Returns:
        bool: True if `file` is a file and exists, False otherwise.
    """
    try:
        file = Path(file)
        return file.is_file() and file.exists()
    except OSError:
        return False


def partition(data: list[T], size: int) -> Iterator[list[T]]:
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


def clean_text(report: str) -> str:
    """Clean a text snippet.

    Args:
        report (str): The text snippet to clean.

    Returns:
        str: The cleaned text snippet (i.e. remove extra spaces and newlines)
    """
    import re

    return re.sub(r"\s+", " ", report).strip()
