==============================================================================
Part 3: Testing Dexterity
==============================================================================

Create simple Dexterity Type
----------------------------

Add Dexterity to the package (setup.py)::

    install_requires=[
        ...
        'plone.app.dexterity',
    ],

Make sure dexterity is installed together with the package::

    <?xml version="1.0"?>
    <metadata>
      <version>1000</version>
      <dependencies>
        <dependency>profile-plone.app.dexterity:default</dependency>
      </dependencies>
    </metadata>

configure.zcml::

    <includeDependencies package="." />

tests/test_task.py:

    $ mkdir profiles/default/types

profiles/default/types/Task.xml:


profiles/default/types.xml::

    <?xml version="1.0"?>
    <object name="portal_types" meta_type="Plone Types Tool">
      <object name="Task" meta_type="Dexterity FTI"/>
    </object>


Integration Test
----------------

tests/test_task.py::

Functional Test
---------------

tests/test_task.py::
