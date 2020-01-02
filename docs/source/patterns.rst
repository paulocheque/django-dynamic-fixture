.. _patterns:

Patterns
*******************************************************************************

Patterns
===============================================================================

  * Use *N* function for unit tests (not integration tests) for the main model.
  * Use *G* function instead of *N* for shelving configurations. It helps to identify errors.
  * Use *ignore_fields* option to deal with fields filled by listeners.
  * Use custom values for unsupported fields.
  * Use default lesson for unsupported fields with a custom function that generated data.
  * Use *fill_nullable_fields* for unsupported nullable fields.
  * Use *number_of_laps* option to test trees.
  * [Automated Test Patterns](http://www.teses.usp.br/teses/disponiveis/45/45134/tde-02042012-120707/pt-br.php) (in Portuguese)

Anti-Patterns
===============================================================================

  * Using auto generated data in an assertion method.
  * Shelving a static value for a field with *unique=True*. Raise an error.
  * Overriding a lesson *Copier* with None.
  * Using *Copier* to fix a bad design of the code.
  * Too many named lessons configurations.
  * Mix data fixture algorithms in the same test suite.
  * Use default and custom lessons to avoid fixing a messy architecture.
  * Extensive use of global set up: setup suite (from DDF), setup module and setup class (from unittest2).


A good automated test
===============================================================================

  * Simple
  * Legible
  * Repeatable
  * Independent
  * Isolated
  * Useful
  * Unique
  * Accurate
  * Professional
  * Fast