"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-s-stewart/
:Date:          2024-03-01
:Compatibility: Python 3.9
:License:       MIT

Combinatorial generation options. These are intended for development and
investigation purposes and are not expected to be exposed at the user level
as the results are unpredictable n that context.
"""

from enum import auto, Flag


class Option(Flag):

    """Options for combinatorial generation.

    :var NONE: No options specified.
    :var NO_SHUFFLE:
    :var FEATURE_RANDOM: Randomise order of features in product generation.
    :var RETIRE_RANDOM: Select the retirement sub-combination randomly.
    """

    NONE = 0
    NO_SHUFFLE = auto()
    FEATURE_RANDOM = auto()
    RETIRE_RANDOM = auto()
