Knuth Generator
===============

+----------+------------+-------------------+--------------------------------+
| Revision | Date       | Author            | Change                         |
+==========+============+===================+================================+
| 1.0      | 2024-04-04 | David Stewart     | Initial Version                |
+----------+------------+-------------------+--------------------------------+

Abstract
--------

The Knuth Generator follows the principles of Knuth's Algorithm X in order to
obtain the best result for a given combination. See `Wikipedia`_.

.. _Wikipedia: https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X

Notes
-----

In this case, the implementation is minimal, only supporting unconstrained
combinatorials with a density of 1.0. This may be extended, however the
scaling behaviour of this technique to this problem set is extremely poor.
