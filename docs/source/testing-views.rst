==============================================================================
Part 4: Testing Views
==============================================================================

Test Simple View
================

.. literalinclude:: ../../src/plonetraining/testing/tests/test_browser_task.py
   :language: python
   :lines: 1-36


Implementation
--------------

browser/configure.zcml:

.. literalinclude:: ../../src/plonetraining/testing/browser/configure.zcml
   :language: xml
   :lines: 7-13

browser/task.py:

.. literalinclude:: ../../src/plonetraining/testing/browser/task.py
   :language: python
   :lines: 1-10

browser/task.pt:

.. literalinclude:: ../../src/plonetraining/testing/browser/task.pt
   :language: html


Test View with Parameter
========================

.. literalinclude:: ../../src/plonetraining/testing/tests/test_browser_task.py
   :language: python
   :lines: 1-10, 39-64


Implementation
--------------

browser/configure.zcml:

.. literalinclude:: ../../src/plonetraining/testing/browser/configure.zcml
   :language: xml
   :lines: 15-21

browser/task.py:

.. literalinclude:: ../../src/plonetraining/testing/browser/task.py
   :language: python
   :lines: 1-10

browser/task.pt:

.. literalinclude:: ../../src/plonetraining/testing/browser/task.pt
   :language: html


Test Protected View
===================

.. literalinclude:: ../../src/plonetraining/testing/tests/test_browser_task.py
   :language: python
   :lines: 1-10, 88-109


Test JSON View
==============

.. literalinclude:: ../../src/plonetraining/testing/tests/test_browser_task.py
   :language: python
   :lines: 1-10, 110-130


Test View Redirect
==================

.. literalinclude:: ../../src/plonetraining/testing/tests/test_browser_task.py
   :language: python
   :lines: 1-10, 110-130

Test::

browser/configure.zcml:

.. literalinclude:: ../../src/plonetraining/testing/browser/configure.zcml
   :language: xml
   :lines: 15-21

browser/task.py:

.. literalinclude:: ../../src/plonetraining/testing/browser/task.py
   :language: python
   :lines: 1-10,47-51

browser/task.pt:

.. literalinclude:: ../../src/plonetraining/testing/browser/task.pt
   :language: html


Troubleshooting
===============

KeyError: 'ACTUAL_URL'
----------------------

Sometimes a view expect an 'ACTUAL_URL' param. If this is the case, make sure you provide the param in the test request::

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']
        self.request.set('URL', self.folder.absolute_url())
        self.request.set('ACTUAL_URL', self.folder.absolute_url())

    def test_view(self):
        view = self.collection.restrictedTraverse('@@RSS')
        self.assertTrue(view())
        self.assertEquals(view.request.response.status, 200)


ComponentLookupError
--------------------

If a view can not be looked up on a particular context, Plone will raise a
ComponentLookupError (because views are multi-adapters), e.g.::

    ComponentLookupError: ((<PloneSite at /plone>, <HTTPRequest, URL=http://nohost/plone>), <InterfaceClass zope.interface.Interface>, 'recipes')::

This can be solved for instance by providing a browser layer that has been
missing::

    def setUp(self):
        self.request = self.layer['request']
        from zope.interface import directlyProvides
        directlyProvides(self.request, IMyCompanyContenttypes)
        ...
