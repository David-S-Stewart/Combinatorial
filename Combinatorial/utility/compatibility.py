"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-stewart-ab643452/
:Date:          2024-03-01
:Compatibility: Python 3.9
:License:       MIT

Methods to maintain backward compatibility.

"""


def bit_count(value: int) -> int:
    """Return the byte count in the integer.

    :param value: The value to get the bit count from.

    Return the number of True bits in the given value.
    """
    try:
        # Introduced in Python 3.10.
        return value.bit_count()
    except Exception:
        return bin(value).count('1')
