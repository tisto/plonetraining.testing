# -*- coding: utf-8 -*-
from plone.app.testing import TEST_USER_ID
from zope.component import queryUtility
from zope.component import createObject
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from plonetraining.testing.testing import PLONETRAINING_TESTING_INTEGRATION_TESTING  # noqa
from plonetraining.testing.interfaces import ITask

import unittest2 as unittest


class TaskIntegrationTest(unittest.TestCase):

    layer = PLONETRAINING_TESTING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Task')
        schema = fti.lookupSchema()
        self.assertEqual(ITask, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Task')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Task')
        factory = fti.factory
        task = createObject(factory)
        self.assertTrue(ITask.providedBy(task))

    def test_adding(self):
        self.portal.invokeFactory('Task', 'task')
        self.assertTrue(ITask.providedBy(self.portal.task))
