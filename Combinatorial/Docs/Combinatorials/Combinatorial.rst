Combinatorial
=============

+----------+------------+-------------------+--------------------------------+
| Revision | Date       | Author            | Change                         |
+==========+============+===================+================================+
| 1.0      | 2024-03-14 | David Stewart     | Initial Version                |
+----------+------------+-------------------+--------------------------------+

Abstract
--------

Full featured n-level combinatorial generator that provides good solutions to
combinatorial selection problems.

This project was borne out of the need to have a performant combinatorial
generator that could be configured natively within Python, rather than as a
separate tool, or as an external executable.

As a result, this combinatorial is designed to work naturally with empty and
single dimensions, which while not mathematically significant are quite common
in programmed scenarios.

Use Cases
---------

Automated test plan management.

Design
------

The combinatorial draws together a range of different heuristics to provide
a full-featured combinatorial tool that is straightforward to configure and
gives good solutions. 

Requirement
-----------

For any generation, the following must hold true:
- All unconstrained sub-combinations must be generated
- There must be no duplicates

There are some desired properties:
- The generation should produce the minimum combinations possible
- The generation should finish in a reasonable time
- Lower order coverages should be complete as early as possible
- The usage of the feature values should be as balanced as possible
