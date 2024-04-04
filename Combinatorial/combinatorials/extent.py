"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-stewart-ab643452/
:Date:          2024-03-01
:Compatibility: Python 3.9
:License:       MIT
"""

from collections.abc import Collection
from typing import Any, Optional
from utility import check
from .dimension import Dimension
from .feature import Feature


class Extent:

    """Extent of a Constraint."""

    def __init__(self, identity: str, values: Collection[Any]):
        """Construct an Extent object.

        :param identity: The identity of the Extent.
        :param values: The values in the Extent.
        """
        assert isinstance(identity, str), check()
        assert isinstance(values, Collection), check()
        # ----------
        self._identity = identity
        self._values = values
        self._dimension = None
        self._features = []

    def evaluate(self) -> bool:
        """True if the Extent evaluates True, False otherwise."""
        return self._dimension.feature in self._features

    @property
    def identity(self) -> str:
        """The identity of the Extent."""
        return self._identity

    @property
    def values(self) -> Collection[Any]:
        """The values in the Extent."""
        return self._values

    @property
    def dimension(self) -> Optional[Dimension]:
        """The dimension referenced by the Extent."""
        return self._dimension

    @dimension.setter
    def dimension(self, value: Optional[Dimension]):
        assert isinstance(value, (Dimension, type(None))), check()
        # ----------
        self._dimension = value
        # Resolve the features.
        self._features = []
        if self._dimension:
            for value in self._values:
                feature = next((f for f in self._dimension.features if
                                f.value == value), None)
                if feature:
                    self._features.append(feature)

    @property
    def features(self) -> list[Feature]:
        """The constraining features from the referenced dimension."""
        return self._features

    def __str__(self) -> str:
        # Example: 'Extent'
        return self.__class__.__name__

    def __eq__(self, other: Any) -> bool:
        # Check equality against another Dimension.
        if type(self) is type(other):
            if self._identity == other.identity:
                if self._value == other.value:
                    if self._dimension == other.dimension:
                        return True
        return False
