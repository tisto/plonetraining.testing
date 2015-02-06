# -*- coding: utf-8 -*-
from plonetraining.testing.testing import PLONETRAINING_TESTING_INTEGRATION_TESTING  # noqa
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

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
        from zope.component import getMultiAdapter
        # Get the view
        view = getMultiAdapter((self.task, self.request), name="view")
        # Put the view into the acquisition chain
        view = view.__of__(self.portal)
        # Call the view
        self.assertTrue(view())
