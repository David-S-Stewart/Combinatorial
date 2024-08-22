Minus One Sequence
==================

+----------+------------+-------------------+--------------------------------+
| Revision | Date       | Author            | Change                         |
+==========+============+===================+================================+
| 1.0      | 2024-08-20 | David Stewart     | Initial Version                |
+----------+------------+-------------------+--------------------------------+

Abstract
--------

The Minus One Sequence recognises that there is always a minimal sequential
solution for any configuration where the coverage is 1 less than the number of
dimensions.

Algorithm
---------

Consider a simple case of a 3 × 3 × 3 generation with a coverage of 2. The
first two columns can be easily generated as the cartesian product, and
this gives the minimum sub-combinations for the solution:

+---+---+---+
| a | b | c |
+===+===+===+
| 0 | 0 |   |
+---+---+---+
| 0 | 1 |   |
+---+---+---+
| 0 | 2 |   |
+---+---+---+
| 1 | 0 |   |
+---+---+---+
| 1 | 1 |   |
+---+---+---+
| 1 | 2 |   |
+---+---+---+
| 2 | 0 |   |
+---+---+---+
| 2 | 1 |   |
+---+---+---+
| 2 | 2 |   |
+---+---+---+

By filling the last dimension with a simple rotation of it's features, the
solution emerges (this validates):

+---+---+---+
| a | b | c |
+===+===+===+
| 0 | 0 | 0 |
+---+---+---+
| 0 | 1 | 1 |
+---+---+---+
| 0 | 2 | 2 |
+---+---+---+
| 1 | 0 | 1 |
+---+---+---+
| 1 | 1 | 2 |
+---+---+---+
| 1 | 2 | 0 |
+---+---+---+
| 2 | 0 | 2 |
+---+---+---+
| 2 | 1 | 0 |
+---+---+---+
| 2 | 2 | 1 |
+---+---+---+

Cases such as 3 × 3 × 2 a straightforward derivations where the features
that are not part the final dimension are simply not expressed. These gaps
can be filled with any valid value without increasing the number of
combinations or invalidating the result:

+---+---+---+
| a | b | c |
+===+===+===+
| 0 | 0 | 0 |
+---+---+---+
| 0 | 1 | 1 |
+---+---+---+
| 0 | 2 |   |
+---+---+---+
| 1 | 0 | 1 |
+---+---+---+
| 1 | 1 |   |
+---+---+---+
| 1 | 2 | 0 |
+---+---+---+
| 2 | 0 |   |
+---+---+---+
| 2 | 1 | 0 |
+---+---+---+
| 2 | 2 | 1 |
+---+---+---+

This principle can be extended to any configuration where the coverage is
one less than the number of dimensions. What is more, the value can be
calculated entirely from the line values, so order of generation and
dimensions does not matter. The algorithm is:
::

	Set cadence to the length of the second smallest dimension.
	Loop through sub-combinations of the dimensions except the smallest:
		Sum of the indexes of the sub-combination.
		Compute the modulus of the sum with respect to cadence.
		If the result is greater than the length of the smallest dimension:
			The smallest dimension is not required.
		Otherwise:
			Set the value of the smallest dimension to the result

This simple algorithm takes into account all the transitions between any
number of dimensions regardless of their respective sizes.

Complexity and Time
-------------------

The complexity is a simple calculation for each generation and is linear.

Memory Usage
------------

There is no memory usage for tracking.
