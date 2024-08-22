Fail Fast
=========

+----------+------------+-------------------+--------------------------------+
| Revision | Date       | Author            | Change                         |
+==========+============+===================+================================+
| 1.0      | 2024-08-20 | David Stewart     | Initial Version                |
+----------+------------+-------------------+--------------------------------+

Abstract
--------

Fail_Fast_ is the decision to fail an operation as early as possible once
detecting an error or inconsistent state. Fail-fast has the advantages that
time is not spent attempting to execute code that is likely invalid, time
is not spent developing extensive error recovery mechanisms, and tends
to lead to problems being identified and repaired more quickly. 

Fail-Fast is conflicts somewhat with Python duck typing which takes pretty
much the opposite approach.

The simplest expression of Fail-Fast is to simply leave the asserts for
pre-conditions on, and failures against the internal interface will fail.

.. _Fail_Fast: https://en.wikipedia.org/wiki/Fail-fast_system
