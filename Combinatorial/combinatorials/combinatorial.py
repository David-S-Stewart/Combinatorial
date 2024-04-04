"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-stewart-ab643452/
:Date:          2024-03-01
:Compatibility: Python 3.9
:License:       MIT
"""

from collections.abc import Generator
from typing import Optional
from .feature import Feature
from .generator import Generator_
from .option import Option
from .knuthgenerator import KnuthGenerator
from .productgenerator import ProductGenerator
from .sequencegenerator import SequenceGenerator


class Combinatorial(Generator_):

    """Combinatorial generator that provides n-level solution sets."""

    def get_features(self) -> Generator[tuple[Feature], None, None]:
        """Return an iterator through the Combinatorial."""
        class_, option = self.get_generator()
        generator = class_(self._dimensions, self._constraints,
                           self._coverage, self._seed)
        generator.option = option
        yield from generator.get_features()

    def get_generator(self) -> tuple[Optional[type], Option]:
        """Get the best generator for the configuration."""
        for case_ in (self.case_1, self.case_2, self.case_3):
            class_, option = case_()
            if class_:
                return class_, option
        return self.case_default()

    def case_default(self) -> tuple[Optional[type], Option]:
        """Return a reasonable default generator."""
        return SequenceGenerator, (Option.COVERAGE_ROTATE_LEFT |
                                   Option.FEATURE_RANDOM)

    def case_1(self) -> tuple[Optional[type], Option]:
        """Return the product generator for configurations where complete
        coverage is required.
        """
        # Any generation where the effective dimensions number the same
        # as the effective coverage can be handled by the product
        # generator.
        if self.effective_coverage == len(self.effective_dimensions):
            return ProductGenerator, Option.FEATURE_RANDOM
        else:
            return None, Option.NONE

    def case_2(self) -> tuple[Optional[type], Option]:
        """Return the sequence generator configured for the special case where
        there are 4 dimensions of 2 features.
        """
        # Special case 2 is where there are 4 dimensions each with 2 features.
        # This case never returns minimum of 4. No solution less than 5 has
        # been found.
        if len(self._dimensions) == 4:
            if len(self._dimensions[0].features) == 2:
                if self.density == 1.0:
                    option = (Option.COVERAGE_SORT_COVERED_MINIMUM |
                              Option.FEATURE_RANDOM)
                    return SequenceGenerator, option
        return None, Option.NONE

    def case_3(self) -> tuple[Optional[type], Option]:
        """Return the Knuth generator configured for very small balanced
        cases.
        """
        # Special case 3 is where the analysis can be reasonably handled by
        # the Knuth generator. With the exception of case 1, these always
        # meet the minimum.
        if not self.constraints:
            if len(self._dimensions) <= 4:
                if len(self._dimensions[0].features) <= 3:
                    if self.density == 1.0:
                        return KnuthGenerator, Option.FEATURE_RANDOM
        return None, Option.NONE
