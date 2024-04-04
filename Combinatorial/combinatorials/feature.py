"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-stewart-ab643452/
:Date:          2024-03-01
:Compatibility: Python 3.9
:License:       MIT
"""

from typing import Any
from utility import check


class Feature:

    """Feature tracking option for a combinatorial Dimension."""

    def __init__(self, index: int, value: Any):
        """Construct a Feature object.

        :param index: The index of the feature.
        :param value: The value of the feature.
        """
        assert isinstance(index, int), check()
        # ----------
        self._index = index
        self._value = value
        self._count = 0

    @property
    def index(self) -> int:
        """The index of the feature."""
        return self._index

    @property
    def value(self) -> Any:
        """The value of the feature."""
        return self._value

    @property
    def count(self) -> int:
        """The usage count of the feature."""
        return self._count

    @count.setter
    def count(self, value: int):
        assert isinstance(value, int), check()
        # ----------
        self._count = value

    def __str__(self) -> str:
        # Example: 'Feature'
        return self.__class__.__name__

    def __eq__(self, other: Any) -> bool:
        # Check equality against another Feature.
        if type(self) is type(other):
            if self._index == other.index:
                if self._value == other.value:
                    return True
        return False
