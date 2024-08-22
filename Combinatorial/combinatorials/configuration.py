"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-s-stewart/
:Date:          2024-08-16
:Compatibility: Python 3.9
:License:       MIT

Provide selection and configuration of generators from user specified values.
"""

from collections.abc import Collection
from typing import Optional
from utility import check
from utility.defaults import NONE_TYPE
from .constraint import Constraint
from .dimension import Dimension
from .fillgenerator import FillGenerator
from .generator import Generator_
from .minusonegenerator import MinusOneGenerator
from .option import Option
from .sequencegenerator import SequenceGenerator


class Configuration:

    """Configuration and selection static methods.

    :var SHUFFLE: Shuffle elements where possible.
    """

    SHUFFLE: bool = True

    @classmethod
    def get_coverage(cls, dimensions: Collection[Dimension] = (),
                     coverage: int = 0) -> int:
        """Select the coverage required for the generator using slice
        notation. The input is taken from the user perspective while the
        output is given from the generator perspective.

        :param dimensions: Dimensions in the configuration.
        :param coverage: Required coverage.
        """
        assert isinstance(dimensions, Collection), check()
        assert isinstance(coverage, int), check()
        # ----------
        # If any dimension is zero length, there can be no combinations.
        if next((True for d in dimensions if len(d) == 0), False):
            return 0
        # Adjust for negative indices and singleton dimensions.
        if coverage < 0:
            coverage = len(dimensions) + coverage
            if coverage <= 0:
                # This must be the minimum coverage which is one.
                return 1
        # Dimensions of length one have no mathematical impact on
        # generation and are excluded for this evaluation.
        dimensions = [d for d in dimensions if len(d) > 1]
        if len(dimensions) == 0:
            # This must also be the minimum coverage which is one.
            return 1
        elif coverage > len(dimensions) or coverage == 0:
            # All effective dimensions are required.
            return len(dimensions)
        else:
            return coverage

    @classmethod
    def get_generator(cls, dimensions: Collection[Dimension] = (),
                      constraints: Collection[Constraint] = (),
                      coverage: int = 0,
                      seed: Optional[int] = None) -> Generator_:
        """Select the best generator for the configuration.

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
        dimensions = [d for d in dimensions if len(d) != 1]
        coverage = cls.get_coverage(dimensions, coverage)
        # Select from deterministic generators.
        for generator in (Generator_, MinusOneGenerator):
            if generator.is_supported(dimensions, constraints, coverage):
                return generator(dimensions, constraints, coverage, seed)
        # Select best non-deterministic generator.
        for generator in (FillGenerator, SequenceGenerator):
            if generator.is_supported(dimensions, constraints, coverage):
                return generator(dimensions, constraints, coverage, seed)
        # This condition should never occur.
        raise Exception('No supporting generators found.')

    @classmethod
    def get_option(cls, generator: Generator_) -> tuple[Option, int]:
        """Get iteration option and seed.

        :param generator: Generator_ to configure.
        """
        option = generator.OPTION
        if not cls.SHUFFLE:
            option |= Option.NO_SHUFFLE
        return option, 0
