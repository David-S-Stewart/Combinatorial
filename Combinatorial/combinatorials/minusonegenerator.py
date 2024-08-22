"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-s-stewart/
:Date:          2024-03-01
:Compatibility: Python 3.9
:License:       MIT

Combinatorial generator for generation where the number of dimensions is
one greater than the coverage and there are no constraints.
"""

from collections.abc import Collection, Generator
from itertools import product
from typing import Optional
from utility import check
from .constraint import Constraint
from .dimension import Dimension
from .feature import Feature
from .generator import Generator_
from .option import Option


class MinusOneGenerator(Generator_):

    """High performance generator that guarantees a minimum number of
    combinations in polynomial time and with very small memory usage. The
    conditions under which this succeeds are:
    - The generator is unconstrained
    - Coverage is 1 less than the number of active dimensions

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
        if constraints:
            return False
        else:
            return len([d for d in dimensions if len(d) > 1]) == coverage + 1

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
        dimensions = list(self._dimensions)
        dimensions.sort(key=lambda d: len(d), reverse=True)
        fixed = self.initialise(dimensions[:self._coverage], option)
        final = dimensions[self._coverage]
        cadence = len(dimensions[self._coverage - 1])
        # Iterate through the combinations.
        for combination in product(*[d.features for d in fixed]):
            count = 0
            for feature, dimension in zip(combination, fixed):
                dimension.feature = feature
                feature.count += 1
                count += feature.index
            count = count % cadence
            if count < len(final):
                final.feature_index = count
                final.feature.count += 1
            else:
                final.feature = None
            yield [d.feature for d in self._dimensions]
