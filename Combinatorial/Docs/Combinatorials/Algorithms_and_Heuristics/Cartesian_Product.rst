Cartesian Product
=================

+----------+------------+-------------------+--------------------------------+
| Revision | Date       | Author            | Change                         |
+==========+============+===================+================================+
| 1.0      | 2024-08-20 | David Stewart     | Initial Version                |
+----------+------------+-------------------+--------------------------------+

Abstract
--------

The Cartesian product is a mathematical operation that returns a set (or a
collection) of ordered pairs or tuples formed by taking elements from two or
more sets. Specifically, if you have two sets A and B, the Cartesian product
of A and B, denoted as A × B, is the set of all possible ordered pairs (a, b)
where a is an element from A and b is an element from B.

Formally:

	**A × B = {(a, b)|a ∈ A and b ∈ B}**

If A has n elements and B has m elements, then A × B will have n × m elements.
For instance, if A={1, 2} and B={x, y}, the Cartesian product A × B would be:

	**A × B = {(1, x),(1, y),(2, x),(2, y)}**

This concept can be extended to more than two sets, such as A × B × C,
resulting in ordered triples, quads, and so on.

Algorithm
---------

The algorithm is a simple matter of iterating through the entire cross
product, removing constrained elements as they occur.

Complexity and Time
-------------------

There is minimum complexity and the time for each generation is linear.

Memory Usage
------------

There is no memory usage for tracking.
