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


Test View HTML Output
=====================

Test::

    from lxml import html
    output = lxml.html.fromstring(view())
    self.assertEqual(len(output.xpath("/html/body/div")), 1)


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


AttributeError: @@plone_portal_state
------------------------------------

todo


Test View Methods
=================

Test::

    def test_method_sections(self):
        self.portal.mi.invokeFactory("Section", id="s1", title="Section 1")
        self.portal.mi.invokeFactory("Section", id="s2", title="Section 2")
        view = getMultiAdapter(
            (self.portal.mi, self.request),
            name="view"
        )
        view = view.__of__(self.portal.mi)

        self.assertEqual(len(view.sections()), 2)
        self.assertEqual(
            [x.title for x in view.sections()]
            [u'Section 1', u'Section 2']
        )


View Status Messages
--------------------

Test::

    def test_delete_comments_sets_status_message(self):
        view = getMultiAdapter(
            (self.portal.mi.se.tc, self.request),
            name="delete"
        )
        view.__of__(self.portal.mi.se)

        view()

        self.assertEqual(
            IStatusMessage(self.request).show()[0].message,
            u'Item deleted'
        )

View Class::

    class DeleteComponent(BrowserView):

        def __call__(self):
            section = aq_parent(self.context)
            section.manage_delObjects([self.context.id])
            IStatusMessage(self.context.REQUEST).addStatusMessage(
                _("Item deleted"),
                type="info"
            )
            self.request.response.redirect(section.absolute_url())

