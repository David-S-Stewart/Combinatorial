"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-s-stewart/
:Date:          2024-03-01
:Compatibility: Python 3.9
:License:       MIT

Provide a user-level combinatorial API.
"""

from collections.abc import Collection, Generator
from typing import Any, Optional
from utility import check
from utility.defaults import NONE_TYPE
from .configuration import Configuration
from .constraint import Constraint
from .dimension import Dimension
from .generator import Generator_


class Combinatorial(Configuration):

    """Combinatorial generator that provides n-level solution sets."""

    def __init__(self, dimensions: Collection[Dimension] = (),
                 constraints: Collection[Constraint] = (),
                 coverage: int = 0, seed: Optional[int] = None):
        """Construct a Combinatorial object.

        :param dimensions: Dimensions in the configuration.
        :param constraints: Constraints in the configuration.
        :param coverage: Required coverage.
        :param seed: Randomising seed.
        """
        assert isinstance(dimensions, Collection), check()
        assert isinstance(constraints, Collection), check()
        assert isinstance(coverage, int), check()
        assert isinstance(seed, (int, NONE_TYPE)), check()
        # ----------
        self._dimensions = dimensions
        self._coverage = coverage
        self._generator = self.get_generator(dimensions, constraints,
                                             coverage, seed)
        super().__init__()

    @property
    def generator(self) -> Generator_:
        """Underlying generator servicing the combinatorial."""
        return self._generator

    @property
    def dimensions(self) -> Collection[Dimension]:
        """Dimensions in the configuration."""
        return self._dimensions

    @property
    def constraints(self) -> Collection[Constraint]:
        """Constraints in the configuration."""
        return self._generator.constraints

    @property
    def coverage(self) -> int:
        """Required coverage."""
        return self._coverage

    @property
    def seed(self) -> Optional[int]:
        """Randomising seed for configuration."""
        return self._generator.seed

    def __iter__(self) -> Generator[tuple[Any], None, None]:
        # iterate through the generator and yield the value sets.
        if next((False for d in self._dimensions if len(d) == 0), True):
            # Return an iterator through the Generator.
            option, iterator_seed = self.get_option(self._generator)
            for _ in self._generator.iterate(option, iterator_seed):
                yield tuple(d.get_value() for d in self._dimensions)
