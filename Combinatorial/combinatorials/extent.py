"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-s-stewart/
:Date:          2024-03-01
:Compatibility: Python 3.9
:License:       MIT

Feature set in the context of a constraint.
"""

from collections.abc import Collection
from typing import Any, Optional
from utility import check
from .dimension import Dimension
from .featureset import FeatureSet


class Extent(FeatureSet):

    """Extent of a Constraint."""

    def __init__(self, identity: str, values: Collection[Any]):
        """Construct an Extent object.

        :param identity: The identity of the Extent.
        :param values: The values in the Extent.
        """
        self._dimension = None
        super().__init__(identity, values)

    def evaluate(self) -> bool:
        """True if the Extent evaluates True, False otherwise."""
        if self._dimension:
            return self._dimension.feature in self._features
        else:
            # If no dimension is set, the extent must evaluate as False.
            return False

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

    def __eq__(self, other: Any) -> bool:
        # Check equality against another Dimension.
        if super().__eq__(other):
            if self._dimension == other.dimension:
                return True
        return False
