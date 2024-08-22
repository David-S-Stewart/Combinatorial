"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-s-stewart/
:Date:          2024-03-01
:Compatibility: Python 3.9
:License:       MIT

Methods to maintain backward compatibility to Python 3.9. Methods defined
here may be removed as older versions of Python fall off the support curve.
"""


def bit_count(value: int) -> int:
    """Return the byte count in the integer.

    :param value: The value to get the bit count from.
    """
    try:
        # Introduced in Python 3.10.
        return value.bit_count()
    except Exception:
        return bin(value).count('1')
