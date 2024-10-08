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
from typing import Optional
from utility import check
from .constraint import Constraint
from .dimension import Dimension
from .feature import Feature
from .generator import Generator_
from .option import Option


class SequenceGenerator(Generator_):

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
        dimensions = list(self._dimensions)
        dimensions.sort(key=lambda d: len(d), reverse=True)
        self.initialise((), option)
        # Iterate through the combinations.
        sub_combinations = self.get_sub_combinations()
        yield from self._fill_to_completion(dimensions, sub_combinations,
                                            option, iterator_seed)
