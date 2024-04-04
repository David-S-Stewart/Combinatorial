Product Generator
=================

+----------+------------+-------------------+--------------------------------+
| Revision | Date       | Author            | Change                         |
+==========+============+===================+================================+
| 1.0      | 2024-04-04 | David Stewart     | Initial Version                |
+----------+------------+-------------------+--------------------------------+

Abstract
--------

The Product Generator follows the observation that any combinatorial where the
minimum length equals the maximum length can be handled simply by looping
through the cross product and excluding the constrained combinations. 

Notes
-----

This is the most efficient generator possible as it maintains very little
state information and utilises efficient Python built-ins.

It is limited to trivial cases, however, these are common in programmed
scenarios.
