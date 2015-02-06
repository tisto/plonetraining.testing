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

Robot Framework Report
----------------------

Robot Framework creates HTML outputs that allows you to investiate test runs and failures. By default, plone.app.robotframework will write three files (log.html, output.xml and report.html into your buildout directory). Open log.html for a full report.

If tests fail, robot framework will automatically create screenshots, to make it easiert to find the problem.


Debugging Robot Framework Tests
-------------------------------

Robot Framework allows you to debug tests in an interactive manner. Just add 'Debug' to any part of the test.

Say you want to debug the 'I am logged in' keyword in the test_example.robot test. Add 'Debug' to the end of the keyword::

    I am logged in
      Wait until page contains  Site Map
      Page should contain  You are now logged in
      Page should contain  admin
      Debug

Then run the test with::

  $ bin/robot src/plonetraining/testing/tests/robot/test_example.robot

The test will open the browser as usual and then stop with an interactive robot shell at the point where you added the 'Debug'::

    ==============================================================================
    Test Example
    ==============================================================================
    Scenario: As a member I want to be able to log into the website ::... ...
    >>>>> Enter interactive shell, only accepted plain text format keyword.
    >

You can now type in robot keywords, e.g.::

    > Page should contain  Home
    >

You can exit the debugger by typing 'exit' and hitting return::

    > exit
    ...

.. note:: The robot debugger currently can not handle special characters and you can not assign and use robot variables. This will hopefully change in the future.


Tagging Robot Framework Tests
-----------------------------

Robot Framework allows us to tag tests with one or more tags::

    Scenario: As a site administrator I can add a Task
      [Tags]  current
      Given a logged-in site administrator
        and an add task form
       When I type 'My Task' into the title field
        and I submit the form
       Then a task with the title 'My Task' has been created

You can then just run robot tests with that tag by providing '-i <tagname>'::

  $ bin/robot -i current src/plonetraining/testing/tests/robot/test_example.robot


Autologin
---------

plone.app.robotframework comes with keywords that allows you to log as different users::

    a logged-in site administrator
      Enable autologin as  Site Administrator

This will login the current user with the 'Site Administrator' role.

It is also possible to login with multiple roles::

    Enable autologin as  Site Administrator  Reviewer

You can logout with::

    Disable Autologin

Or set the username with::

    Set Autologin Username  john


Create Content
--------------

plone.app.robotframework comes with keywords to create content::

  Create content  type=Task  id=my-task  title=My Task

This creates a 'Task' content object with the id 'my-task' and the title 'My Task'.

Screenshots
-----------

You can capture screenshots during your robot framework tests that you can ,for instance, use in your docs::

Scenario: Capture Screenshot of the Login Form
  [Tags]  screenshot
  Go To  ${PLONE_URL}/login_form
  Capture Page Screenshot  filename=login_form.png

.. note:: See http://datakurre.pandala.org/2013/04/generate-annotated-screenshots-with.html for how to generate annotated screenshots with Robot Framework.

Further Reading
---------------

- todo: how to write good robot framework tests.
