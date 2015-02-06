==============================================================================
Part 3: Testing Dexterity
==============================================================================

Create simple Dexterity Type
----------------------------

Add Dexterity to the package (setup.py):

.. literalinclude:: ../../setup.py
   :language: python
   :lines: 43-48
   :emphasize-lines: 45-47


Make sure dexterity is installed together with the package:

.. literalinclude:: ../../src/plonetraining/testing/profiles/default/metadata.xml
   :language: xml
   :emphasize-lines: 5


configure.zcml::

    <includeDependencies package="." />

Create profiles/default/types directory::

    $ mkdir profiles/default/types

Create Factory Type Information (FTI) for Task Type (profiles/default/types/Task.xml):

.. literalinclude:: ../../src/plonetraining/testing/profiles/default/types/Task.xml
   :language: xml

Include Task FTI in Generic Setup Profile (profiles/default/types.xml):

.. literalinclude:: ../../src/plonetraining/testing/profiles/default/types.xml
   :language: xml


Interface
---------

interfaces.py:

.. literalinclude:: ../../src/plonetraining/testing/interfaces.py
   :language: python

Integration Test
----------------

tests/test_task.py:

.. literalinclude:: ../../src/plonetraining/testing/tests/test_task.py
   :language: python
   :lines: 1-43
   :emphasize-lines: 19


Functional Test
---------------

tests/test_task.py:

.. literalinclude:: ../../src/plonetraining/testing/tests/test_task.py
   :language: python
   :lines: 1-15,44-
   :emphasize-lines: 47


Robot Test
----------

tests/robot/test_task.robot:

.. literalinclude:: ../../src/plonetraining/testing/tests/robot/test_task.robot
   :language: robotframework
   :emphasize-lines: 37
