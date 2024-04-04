BitArray
========

+----------+------------+-------------------+--------------------------------+
| Revision | Date       | Author            | Change                         |
+==========+============+===================+================================+
| 1.0      | 2024-03-03 | David Stewart     | Initial Version                |
+----------+------------+-------------------+--------------------------------+

Abstract
--------

A BitArray is a collection class that implements the Collection interface for
truth values in a memory efficient manner.

Use Cases
---------

Large scale indexed boolean flag array.

Design
------

Implemented as a class with two properties, a bytearray where each byte
represents 8 bits and an integer representing the length.

The array is maintained at the minimum possible length. Where the length of
the array is not divisible by 8, the final byte in the array is padded with
False values.

The BitArray extends the Collection class and implements much of the list
class as well, excluding sort and remove which do not make a lot of sense
in this context.

An invert method has also been added.

Test Strategy
-------------

Where a function mirrors one in the list implementation, testing directly
against list functionality gives consistent behaviour. This assumes that
the list behaviour is the standard.

Improvements
------------

- Modify BitArray.extend to construct negative indexes as truths.
- Modify BitArray.extend to utilise bit shift.
- Modify BitArray.index to search for a target by byte.
- Modify BitArray.invert to operate a byte at a time.
