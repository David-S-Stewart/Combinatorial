"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-stewart-ab643452/
:Date:          2024-03-01
:Compatibility: Python 3.9
:License:       MIT
"""

from collections.abc import Collection
from typing import Any
from utility import check
from .extent import Extent


class Constraint:

    """Constraint against a combinatorial generator."""

    def __init__(self, extents: Collection[Extent]):
        """
        Construct a Constraint object.

        :param extents: Extents of the Constraint.
        """
        assert isinstance(extents, Collection), check()
        # ----------
        self._extents = extents

    def evaluate(self) -> bool:
        """True if the Constraint evaluates True, False otherwise."""
        return next((False for e in self.extents if not e.evaluate()), True)

    @property
    def extents(self) -> Collection[Extent]:
        """Extents of the Constraint."""
        return self._extents

    def __str__(self) -> str:
        # Example: 'Constraint'
        return self.__class__.__name__

    def __eq__(self, other: Any) -> bool:
        # Check equality against another Constraint.
        if type(self) is type(other):
            if self._extents == other.extents:
                return True
        return False
