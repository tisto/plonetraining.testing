# -*- coding: utf-8 -*-
from zope.component import getMultiAdapter
from plonetraining.testing.testing import PLONETRAINING_TESTING_INTEGRATION_TESTING  # noqa
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing import logout

import unittest2 as unittest


class TaskViewIntegrationTest(unittest.TestCase):

    layer = PLONETRAINING_TESTING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Task', id='task', title='Task')
        self.task = self.portal.task

    def test_view_with_get_multi_adapter(self):
        # Get the view
        view = getMultiAdapter((self.task, self.request), name="view")
        # Put the view into the acquisition chain
        view = view.__of__(self.portal)
        # Call the view
        self.assertTrue(view())

    def test_view_with_restricted_traverse(self):
        view = self.task.restrictedTraverse('view')
        self.assertTrue(view())

    def test_view_with_unrestricted_traverse(self):
        view = self.task.unrestrictedTraverse('view')
        self.assertTrue(view())

    def test_view_with_browserlayer(self):
        # Make the request provide the browser layer so our view can be looked
        # up
        from zope.interface import directlyProvides
        from plonetraining.testing.interfaces import IPlonetrainingTestingLayer
        directlyProvides(self.request, IPlonetrainingTestingLayer)
        # Get the view
        view = getMultiAdapter(
            (self.task, self.request),
            name="view-with-browserlayer"
        )
        # Put the view into the acquisition chain
        view = view.__of__(self.portal)
        # Call the view
        self.assertTrue(view())

    def test_view_with_request_parameter(self):
        self.request.set('term', 'foo')
        view = getMultiAdapter(
            (self.task, self.request),
            name="view-with-params"
        )
        view = view.__of__(self.portal)
        self.failUnless(view())

    def test_view_protected(self):
        """Try to access a protected view and make sure we raise Unauthorized.
        """
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(
            Unauthorized,
            self.task.restrictedTraverse,
            'view-protected'
        )
