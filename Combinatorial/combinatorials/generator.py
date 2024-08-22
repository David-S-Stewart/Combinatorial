"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-s-stewart/
:Date:          2024-03-01
:Compatibility: Python 3.9
:License:       MIT

Core combinatorial generator that supports all generations where the number
of dimension equals the coverage.
"""

from collections.abc import Collection, Generator
from itertools import combinations, product
from math import prod
from random import Random
from typing import Any, Optional
from utility import check
from utility.defaults import NONE_TYPE
from .constraint import Constraint
from .dimension import Dimension
from .feature import Feature
from .option import Option
from .subcombination import SubCombination


class Generator_:

    """Base Generator that defines generator characteristics and supports
    all generations that can be satisfied by the cartesian product.

    :var OPTION: Default option for this generator.
    """

    OPTION: Option = Option.NONE

    @classmethod
    def is_supported(cls, dimensions: Collection[Dimension],
                     constraints: Collection[Constraint],
                     coverage: int) -> bool:
        """True if the generator supports this configuration, False otherwise.

        :param dimensions: Dimensions in the configuration.
        :param constraints: Constraints in the configuration.
        :param coverage: Required coverage.
        """
        # Any valid configuration only requires all dimensions to be covered.
        if dimensions:
            if next((True for d in dimensions if len(d) == 0), False):
                return True
            else:
                return len(dimensions) == coverage
        else:
            return True

    def __init__(self, dimensions: Collection[Dimension],
                 constraints: Collection[Constraint],
                 coverage: int, seed: Optional[int] = None):
        """Construct a Generator_ object.

        :param dimensions: Dimensions in the configuration.
        :param constraints: Constraints in the configuration.
        :param coverage: Required coverage.
        :param seed: Randomising seed.
        """
        assert isinstance(dimensions, Collection), check()
        # The generators do not support dimensions with less than 2 features.
        assert next((False for d in dimensions if len(d) == 1), True)
        assert isinstance(constraints, Collection), check()
        # Coverage must be in range.
        assert isinstance(coverage, int), check()
        if len(dimensions) == 0:
            assert coverage == 1, check()
        elif next((True for d in dimensions if len(d) == 0), False):
            assert coverage == 0, check()
        else:
            assert 0 < coverage <= len(dimensions), check()
        assert isinstance(seed, (int, NONE_TYPE)), check()
        assert self.is_supported(dimensions, constraints, coverage), check()
        # ----------
        self._dimensions = dimensions
        self._constraints = constraints
        self._coverage = coverage
        self._seed = seed

    def initialise(self, dimensions: Collection[Dimension] = (),
                   option: Option = OPTION) -> list[Dimension]:
        """Initialise the dimensions in the Generator_. This is the sole user
        of the seed property and initialises feature and dimension order.

        :param dimensions: Dimensions for randomisation.
        :param option: Option for this iteration.
        """
        random = None if option & Option.NO_SHUFFLE else Random(self._seed)
        # Initialise the dimensions.
        for dimension in self._dimensions:
            dimension.initialise(random)
        # Index constraints.
        for constraint in self._constraints:
            for extent in constraint.extents:
                extent.dimension = next((d for d in self._dimensions if
                                         extent.identity == d.identity), None)
        # Shuffle and return optional dimensions.
        dimensions = list(dimensions)
        if random:
            random.shuffle(dimensions)
        return dimensions

    def get_sub_combinations(self) -> list[SubCombination]:
        """Get a set of SubCombinations for the required coverage level.

        Initial order for the sub-combinations is based on length, high to
        low.
        """
        # Generate the sub_combinations.
        if self._dimensions:
            sub_combinations = [SubCombination(c) for c in
                                combinations(self._dimensions,
                                             self._coverage)]
            # Pre-apply constraints.
            for sub_combination in sub_combinations:
                for constraint in self._constraints:
                    sub_combination.apply_constraint(constraint)
            # Sort and return.
            sub_combinations.sort(key=lambda s: s.count(False), reverse=True)
            return sub_combinations
        else:
            return []

    def is_constrained(self) -> bool:
        """True if the current combination is constrained, False otherwise."""
        return next((True for c in self._constraints if c.evaluate()), False)

    def iterate(self, option: Option = OPTION, iterator_seed: int = 0) \
            -> Generator[Collection[Optional[Feature]], None, None]:
        """Iterate through a set of combinations that satisfy this
        generation.

        :param option: Option for this iteration.
        :param iterator_seed: Randomising seed for iteration.
        """
        assert isinstance(option, Option), check()
        assert isinstance(iterator_seed, int), check()
        # ----------
        dimensions = self.initialise(self._dimensions, option)
        # Iterate through the combinations.
        for combination in product(*[d.features for d in dimensions]):
            for feature, dimension in zip(combination, dimensions):
                dimension.feature = feature
            if not self.is_constrained():
                for feature in combination:
                    feature.count += 1
                yield [d.feature for d in dimensions]

    @property
    def dimensions(self) -> Collection[Dimension]:
        """Dimensions in the configuration."""
        return self._dimensions

    @property
    def constraints(self) -> Collection[Constraint]:
        """Constraints in the configuration."""
        return self._constraints

    @property
    def coverage(self) -> int:
        """Required coverage."""
        return self._coverage

    @property
    def seed(self) -> Optional[int]:
        """Randomising seed."""
        return self._seed

    @property
    def minimum(self) -> int:
        """Minimum length possible for unconstrained generation."""
        if self.maximum == 0:
            return 0
        else:
            dimensions = sorted(self.dimensions,
                                key=lambda d: len(d), reverse=True)
            return prod(len(d) for d in dimensions[:self._coverage])

    @property
    def maximum(self) -> int:
        """Maximum length possible for unconstrained generation."""
        return prod(len(d) for d in self.dimensions)

    def __str__(self) -> str:
        # Example: 'Generator_'
        return self.__class__.__name__

    def __eq__(self, other: Any) -> bool:
        # Check equality against another Generator_.
        if type(self) is type(other):
            if self._dimensions == other.dimensions:
                if self._constraints == other.constraints:
                    if self._coverage == other.coverage:
                        if self._seed == other._seed:
                            return True
        return False

    def _fill_to_completion(self, dimensions: list[Dimension],
                            sub_combinations: list[SubCombination],
                            option: Option, iterator_seed: int) \
            -> Generator[Collection[Optional[Feature]], None, None]:
        # Yield sub-combinations to completion. This uses a best fill
        # heuristic that does not attempt to maintain combination to
        # combination order.

        # Select feature order.
        random = Random(iterator_seed)
        order = random if option & Option.FEATURE_RANDOM else None

        while sub_combinations:
            # Select the next sub_conbination to retire.
            retire = sub_combinations[0]
            if option & Option.RETIRE_RANDOM:
                retire.sub_combination_index = retire.random_index(False,
                                                                   random)
            else:
                retire.sub_combination_index = retire.index(False)
            variable = [d for d in dimensions if d not in retire.dimensions]
            # Resolve a solution.
            best = []
            count = len(sub_combinations)
            for solution in product(*[d.get_features(order)
                                      for d in variable]):
                for feature, dimension in zip(solution, variable):
                    dimension.feature = feature
                if not self.is_constrained():
                    covered = sum(1 for s in sub_combinations if s.is_covered)
                    if covered == 0:
                        count = 0
                        best = solution
                        break
                    elif covered < count:
                        count = covered
                        best = solution
            if best:
                if count > 0:
                    # Reload best.
                    for feature, dimension in zip(best, variable):
                        dimension.feature = feature
                # Cover the solution and yield.
                for sub_combination in sub_combinations:
                    sub_combination.cover()
                for dimension in dimensions:
                    dimension.feature.count += 1
                yield [d.feature for d in self._dimensions]
            else:
                # In this case there is no unconstrained solution for the
                # retiring sub-combination.
                retire.cover()
            # Remove complete sub_combinations.
            sub_combinations = [s for s in sub_combinations if False in s]
