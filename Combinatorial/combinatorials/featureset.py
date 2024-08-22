"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-s-stewart/
:Date:          2024-08-16
:Compatibility: Python 3.9
:License:       MIT

Core collection of features.
"""

from collections.abc import Collection
from typing import Any
from utility import check
from .feature import Feature


class FeatureSet:

    """"""

    def __init__(self, identity: str, values: Collection[Any]):
        """Construct a FeatureSet object.

        :param identity: The identity of the FeatureSet.
        :param values: The values in the FeatureSet.
        """
        assert isinstance(identity, str), check()
        assert isinstance(values, Collection), check()
        # ----------
        self._identity = identity
        self._values = values
        self._features = []

    @property
    def identity(self) -> str:
        """The identity of the FeatureSet."""
        return self._identity

    @property
    def values(self) -> Collection[Any]:
        """The values in the FeatureSet."""
        return self._values

    @property
    def features(self) -> list[Feature]:
        """Indexed Features of the FeatureSet."""
        return self._features

    def __str__(self) -> str:
        # Example: 'Dimension 1, 3 feature(s)'
        return f'{self._identity}, {len(self._values)} feature(s)'

    def __eq__(self, other: Any) -> bool:
        # Check equality against another FeatureSet.
        if type(self) is type(other):
            if self._identity == other.identity:
                if self._value == other.value:
                    return True
        return False

    def __len__(self) -> int:
        # Return length of the FeatureSet.
        return len(self._values)
