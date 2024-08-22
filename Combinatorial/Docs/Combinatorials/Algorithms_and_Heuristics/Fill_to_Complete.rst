Fill to Complete
================

+----------+------------+-------------------+--------------------------------+
| Revision | Date       | Author            | Change                         |
+==========+============+===================+================================+
| 1.0      | 2024-08-20 | David Stewart     | Initial Version                |
+----------+------------+-------------------+--------------------------------+

Abstract
--------

The Fill to Complete heuristic is the most general generator and is designed
to provide good, if not perfect, performance across the entire problem domain.

On its own, this heuristic gives results comparable with other solutions.

Heuristic
---------

The heuristic begins by creating a set of coverage data for each
sub_combination of the effective dimensions at the coverage levels. The
Coverage object extends the BitArray to provide a tracking bit for each
sub_combination.

A loop is run selecting a sub-combination to retire each iteration, with as
many other sub-combinations being retired as well. These are found by
testing against a cartesian product of the remaining dimensions until either
a maximum is found or there are no more candidates, in which case the best
result is chosen. 

The selection of an sub-combination that is not already covered guarantees
that the completed combination cannot have already been yielded.

A minimum of one sub-combination must be retired each loop so the loop cannot
be infinite. Once tracking indicates that all required sub-combinations have
been covered, the generation exits.

Complexity and Time
-------------------

Time requirements rise significantly faster than the number of combinations.

Memory Usage
------------

Coverage tracking takes one bit per sub-combination (with a little overflow).
