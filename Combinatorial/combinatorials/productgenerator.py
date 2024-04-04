"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-stewart-ab643452/
:Date:          2024-03-01
:Compatibility: Python 3.9
:License:       MIT
"""

from collections.abc import Generator
from itertools import product
from random import Random
from .feature import Feature
from .generator import Generator_


class ProductGenerator(Generator_):

    """Generator that provides n-level solution sets using the product
    generator tool.
    """

    def get_features(self) -> Generator[tuple[Feature], None, None]:
        """Return an iterator through the ProductGenerator."""
        if self.effective_coverage != len(self.effective_dimensions):
            raise Exception(f'{self.__class__.__name__} only supports full '
                            f'generation [{self.effective_coverage} != '
                            f'{len(self.effective_dimensions)}].')
        else:
            random = Random(self._seed)
            for features in product(*[d.select(random) for d in
                                      self._dimensions]):
                for feature, dimension in zip(features, self._dimensions):
                    dimension.feature = feature
                if not self.is_constrained():
                    yield features
