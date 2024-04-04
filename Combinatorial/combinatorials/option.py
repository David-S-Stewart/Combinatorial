"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-stewart-ab643452/
:Date:          2024-03-01
:Compatibility: Python 3.9
:License:       MIT
"""

from enum import auto, Flag


class Option(Flag):

    """ Options for combinatorial generation.

    :var NONE: No options specified.
    :var FEATURE_RANDOM: Randomise order of features in product generation.
    :var FEATURE_COUNT_MINIMUM: Order features for product generation by use.
    :var FEATURE_COUNT_MAXIMUM: Order features for product generation by use.
    :var RETIRE_RANDOM: Select the retirement sub-combination randomly.
    :var COVERAGE_SHUFFLE: Shuffle the coverages randomly.
    :var COVERAGE_ROTATE_LEFT: Rotate the coverages left.
    :var COVERAGE_ROTATE_RIGHT: Rotate the coverages right.
    :var COVERAGE_SORT_COVERED_MINIMUM: Sort the coverages by covered minimum.
    :var COVERAGE_SORT_COVERED_MAXIMUM: Sort the coverages by covered maximum.
    :var COVERAGE_SORT_REMAINING_MINIMUM: Sort the coverages by remaining
                                          minimum.
    :var COVERAGE_SORT_REMAINING_MAXIMUM: Sort the coverages by remaining
                                          maximum.
    """

    NONE = 0
    FEATURE_RANDOM = auto()
    FEATURE_COUNT_MINIMUM = auto()
    FEATURE_COUNT_MAXIMUM = auto()
    RETIRE_RANDOM = auto()
    COVERAGE_SHUFFLE = auto()
    COVERAGE_ROTATE_LEFT = auto()
    COVERAGE_ROTATE_RIGHT = auto()
    COVERAGE_SORT_COVERED_MINIMUM = auto()
    COVERAGE_SORT_COVERED_MAXIMUM = auto()
    COVERAGE_SORT_REMAINING_MINIMUM = auto()
    COVERAGE_SORT_REMAINING_MAXIMUM = auto()
