Design by Contract
==================

+----------+------------+-------------------+--------------------------------+
| Revision | Date       | Author            | Change                         |
+==========+============+===================+================================+
| 1.0      | 2024-08-20 | David Stewart     | Initial Version                |
+----------+------------+-------------------+--------------------------------+

Abstract
--------

At its most basic, Design_by_Contract_ (DbC) asserts that a component method
given a valid input will give a valid output and leave the component in a
valid state.

Design by contract states that, in production, interfaces should not be
checked as this is a performance drag and the checking performs no operational
objective, although pre-conditions are often left operational for Fail Fast
reasons.

At it's most basic, the contract is stated in the following ways:

- Documentation in the code base
- Type hints

DbC naturally specifies good unit tests.

In larger systems, I use decorators to test all three elements (at a typing
level at least) but for smaller stand-alone components, asserts for
pre-conditions are provided. These can be disabled by using the -O
directive. 

.. _Design_by_Contract: https://en.wikipedia.org/wiki/Design_by_contract
