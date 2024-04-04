"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-stewart-ab643452/
:Date:          2024-03-01
:Compatibility: Python 3.9
:License:       MIT
"""

from collections.abc import Collection, Generator
from itertools import combinations
from math import prod
from random import Random
from typing import Any, Optional
from utility import check
from .constraint import Constraint
from .coverage import Coverage
from .dimension import Dimension
from .feature import Feature
from .option import Option


class Generator_:

    """Abstract generator that provides n-level solution sets."""

    def __init__(self, dimensions: Collection[Dimension],
                 constraints: Collection[Constraint] = (),
                 coverage: int = 0, seed: Optional[int] = None):
        """Construct a Generator_ object.

        :param dimensions: Dimensions of the Generator_.
        :param constraints: Constraints on the Generator_.
        :param coverage: Dimension coverage required.
        :param seed: Randomising seed.
        """
        assert isinstance(dimensions, Collection), check()
        assert isinstance(constraints, Collection), check()
        assert isinstance(coverage, int), check()
        assert isinstance(seed, (int, type(None))), check()
        # ----------
        self._dimensions = dimensions
        self._constraints = constraints
        self._coverage = coverage
        self._seed = seed
        self._option = Option.NONE
        # Index dimensions.
        for index, dimension in enumerate(self._dimensions):
            dimension.index = index
        # Index constraints.
        for constraint in self._constraints:
            for extent in constraint.extents:
                extent.dimension = next((d for d in self._dimensions if
                                         extent.name == d.name), None)

    def get_coverages(self) -> list[Coverage]:
        """Get a set of coverages for the required coverage level."""
        return [Coverage(c, self._option) for c in
                combinations(self.effective_dimensions,
                             self.effective_coverage)]

    def is_constrained(self) -> bool:
        """True if the current combination is constrained, False otherwise."""
        return next((True for c in self._constraints if c.evaluate()), False)

    def get_features(self) -> Generator[tuple[Feature], None, None]:
        """Return an iterator through the Generator_."""
        raise NotImplementedError('Abstract interface.')

    def validate(self):
        """Validate the generator.

        Duplicates are tested by checking that a single encompassing Coverage
        never records a duplicate.

        For unconstrained generators, a standard set of coverages will have
        no uncovered coverage combination at the end of a generation.
        """
        if len(self.effective_dimensions) > 0:
            duplicates = Coverage(self.effective_dimensions)
            coverages = self.get_coverages()
            for _ in self.get_features():
                if duplicates.is_covered():
                    raise Exception('Some combinations duplicated.')
                duplicates.cover()
                for coverage in coverages:
                    coverage.cover()
            if not self._constraints:
                for coverage in coverages:
                    if False in coverage:
                        text = 'Some required combinations not covered.'
                        raise Exception(text)

    def display(self) -> str:
        """"""
        return (f'Dimensions:       {len(self.effective_dimensions)}\n'
                f'Constraints:      {len(self._constraints)}\n'
                f'Coverage:         {self.effective_coverage}\n'
                f'Minimum:          {self.minimum_length}\n'
                f'Maximum:          {self.maximum_length}\n'
                f'Sub-combinations: {self.sub_combinations}\n'
                f'Density:          {self.density}')

    @property
    def dimensions(self) -> Collection[Dimension]:
        """Dimensions of the Generator_."""
        return self._dimensions

    @property
    def effective_dimensions(self) -> list[Dimension]:
        """Number of effective dimensions in the combinatorial."""
        return [d for d in self._dimensions if len(d) > 1]

    @property
    def constraints(self) -> Collection[Constraint]:
        """Constraints on the Generator_."""
        return self._constraints

    @property
    def coverage(self) -> int:
        """Dimension coverage required."""
        return self._coverage

    @property
    def effective_coverage(self) -> int:
        """Effective coverage."""
        length = len(self.effective_dimensions)
        if length == 0:
            return 0
        if self._coverage:
            if self._coverage > length:
                return length
            elif self._coverage < 0:
                if -self._coverage >= length:
                    return 1
                else:
                    return length + self._coverage
            else:
                return self._coverage
        else:
            return length

    @property
    def sub_combinations(self) -> int:
        """Number of sub-combinations to cover."""
        coverages = self.get_coverages()
        return sum(len(c) for c in coverages)

    @property
    def sub_coverages(self) -> int:
        """Number of coverages required for generation."""
        return len(list(combinations(self.effective_dimensions,
                                     self._coverage)))

    @property
    def density(self) -> float:
        """Density of sub_combinations required for minimum."""
        if self.sub_coverages == 0 or self.minimum_length == 0:
            return 1.0
        else:
            return (self.sub_combinations
                    / self.sub_coverages
                    / self.minimum_length)

    @property
    def minimum_length(self) -> int:
        """Minimum length possible for unconstrained generation."""
        if self.maximum_length == 0:
            # In this case there is a zero-length dimension and there
            # cannot be any valid combinations.
            return 0
        else:
            return prod(sorted(len(d) for d in
                               self._dimensions)[-self._coverage:])

    @property
    def maximum_length(self) -> int:
        """Maximum length possible for unconstrained generation."""
        return prod(len(v) for v in self.dimensions)

    @property
    def seed(self) -> Optional[int]:
        """Randomising seed."""
        return self._seed

    @property
    def option(self) -> Option:
        """Generation option set for the Generator_."""
        return self._option

    @option.setter
    def option(self, value: Option):
        assert isinstance(value, Option), check()
        # ----------
        self._option = value
        for dimension in self._dimensions:
            dimension.option = value

    def __str__(self) -> str:
        # Example: 'Generator_'
        return self.__class__.__name__

    def __eq__(self, other: Any) -> bool:
        # Check equality against another Generator_.
        if type(self) is type(other):
            if self._dimensions == other.dimensions:
                if self._constraints == other.constraints:
                    if self._coverage == other.coverage:
                        if self._seed == other.seed:
                            return True
        return False

    def __iter__(self) -> Generator[tuple[Any], None, None]:
        # Return an iterator through the Generator.
        for features in self.get_features():
            yield tuple(f.value for f in features)

    def _clear(self):
        # Clear the feature counts.
        for dimension in self._dimensions:
            for feature in dimension.features:
                feature.count = 0

    def _order_coverages(self, coverages: list[Coverage], random: Random):
        # Order coverages according to the option.
        if self._option & Option.COVERAGE_SHUFFLE:
            random.shuffle(coverages)
        elif self._option & Option.COVERAGE_ROTATE_LEFT:
            coverage = coverages.pop(0)
            coverages.append(coverage)
        elif self._option & Option.COVERAGE_ROTATE_RIGHT:
            coverage = coverages.pop()
            coverages.insert(0, coverage)
        elif self._option & Option.COVERAGE_SORT_COVERED_MINIMUM:
            coverages.sort(key=lambda c: c.count(True))
        elif self._option & Option.COVERAGE_SORT_COVERED_MAXIMUM:
            coverages.sort(key=lambda c: c.count(True), reverse=True)
        elif self._option & Option.COVERAGE_SORT_REMAINING_MINIMUM:
            coverages.sort(key=lambda c: c.count(False))
        elif self._option & Option.COVERAGE_SORT_REMAINING_MAXIMUM:
            coverages.sort(key=lambda c: c.count(False), reverse=True)
