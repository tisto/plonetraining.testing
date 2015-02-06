==============================================================================
Part 7: Robot Framework
==============================================================================

Robot Framework Setup
---------------------

Add plone.app.robotframework to the package dependencies in setup.py:

.. literalinclude:: ../../setup.py
   :language: python
   :lines: 51-57
   :emphasize-lines: 55

Add plone.app.robotframework to your buildout configuration:

.. literalinclude:: ../../buildout.d/development.cfg
   :language: python
   :lines: 38-43
   :emphasize-lines: 55

Add a robot framework testing fixture to your test setup:

.. literalinclude:: ../../src/plonetraining/testing/testing.py
   :language: python
   :lines: 51-58
   :emphasize-lines: 55

Add a python file that automatically looks up all your robot tests in the 'robots folder and runs them within your test suite:

.. literalinclude:: ../../src/plonetraining/testing/tests/test_robot.py
   :language: python

.. note:: robottestsuite.level assign all your robot test to a higher zope.testrunner test level. That means that your robot tests are not run by default (e.g. if you run 'bin/test'. In order to run your robot tests you have to tell the zope.testrunner to run all test level (e.g. with 'bin/test --all). This way you can exclude the long-running robot test when running your other tests.

Add a first robot test:

.. literalinclude:: ../../src/plonetraining/testing/tests/robot/test_example.robot
   :language: python

Run Robot Tests
---------------

Start the robot-server::

  $ bin/robot-server --reload-path src plonetraining.testing.testing.PLONETRAINING_TESTING_ACCEPTANCE_TESTING

.. note:: --reload-path will automatically reload your changes to Python code, so you don't have to restart the robot server.

Run the robot tests::

  $ bin/robot src/plonetraining/testing/tests/robot/test_example.robot

You can also run the robot test 'stand-alone' without robot-server. Though, this will take more time::

  $ bin/test -t test_example --all
