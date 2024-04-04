Sequence Generator
===================

+----------+------------+-------------------+--------------------------------+
| Revision | Date       | Author            | Change                         |
+==========+============+===================+================================+
| 1.0      | 2024-04-04 | David Stewart     | Initial Version                |
+----------+------------+-------------------+--------------------------------+

Abstract
--------

The Sequence Generator is the most general generator and is designed to
provide good, if not perfect, performance across the entire problem domain.

Heuristic
---------

The heuristic begins by creating a set of coverage data for each combination
of the effective dimensions at the coverage levels. The Coverage object
extends the BitArray and provides a tracking bit and conversion methods
for each required sub-combination.

A loop is run selecting a sub-combination to retire each iteration, with as
many other sub-combinations being retired as well. A minimum of one
sub-combination must be retired each loop so the loop cannot be infinite.
Once all Coverage tracking indicates that all required sub-combinations have
been covered, the generation exits.

A range of sort and select options are provided, and the Combinatorial class
selects among these based on the configuration.
 