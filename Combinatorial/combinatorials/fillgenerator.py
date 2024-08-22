"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-s-stewart/
:Date:          2024-03-01
:Compatibility: Python 3.9
:License:       MIT

Combinatorial generator for generation where the number of dimensions is
greater than the coverage.
"""

from collections.abc import Collection, Generator
from itertools import product
from random import Random
from typing import Optional
from utility import check
from .constraint import Constraint
from .dimension import Dimension
from .feature import Feature
from .generator import Generator_
from .minusonegenerator import MinusOneGenerator
from .option import Option


class FillGenerator(Generator_):

    """General purpose generator that can resolve all generations except those
    covered by the Generator_.

    :var OPTION: Default option for this generator.
    """

    OPTION: Option = Option.FEATURE_RANDOM | Option.RETIRE_RANDOM

    @classmethod
    def is_supported(cls, dimensions: Collection[Dimension],
                     constraints: Collection[Constraint],
                     coverage: int) -> bool:
        """True if the generator supports this configuration, False otherwise.

        :param dimensions: Dimensions in the configuration.
        :param constraints: Constraints in the configuration.
        :param coverage: Required coverage.
        """
        return not Generator_.is_supported(dimensions, constraints, coverage)

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
        dimensions = [d for d in self._dimensions if len(d) > 1]
        dimensions.sort(key=lambda d: len(d), reverse=True)
        minus = MinusOneGenerator(dimensions[:self._coverage + 1],
                                  (), self._coverage)
        variable = dimensions[self._coverage:]
        self.initialise((), option)
        # Iterate through the combinations.
        sub_combinations = self.get_sub_combinations()
        # Select feature order.
        random = Random(iterator_seed)
        order = random if option & Option.FEATURE_RANDOM else None
        for features in minus.iterate(option, iterator_seed):
            # Select feature order.
            best = []
            count = len(sub_combinations)
            feature_sets = [d.get_features(order) for d in variable]
            if features[-1] is not None:
                feature_sets[0] = [features[-1]]
            for solution in product(*feature_sets):
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
                # Remove complete sub_combinations.
                sub_combinations = [s for s in sub_combinations if False in s]

        # Use the complete method to fill the remaining sub_combinations.
        yield from self._fill_to_completion(dimensions, sub_combinations,
                                            option, iterator_seed)
