# -*- coding: utf-8 -*-
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser
from plone.app.testing import TEST_USER_ID
from zope.component import queryUtility
from zope.component import createObject
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from plonetraining.testing.testing import PLONETRAINING_TESTING_FUNCTIONAL_TESTING  # noqa
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


class TaskFunctionalTest(unittest.TestCase):

    layer = PLONETRAINING_TESTING_FUNCTIONAL_TESTING

    def setUp(self):
        app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portal_url = self.portal.absolute_url()

        # Set up browser
        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )

    def test_add_task(self):
        self.browser.open(self.portal_url + '/++add++Task')
        self.browser.getControl(name="form.widgets.title").value = \
            "My Task"
        self.browser.getControl(name="form.widgets.description")\
            .value = "This is my task"
        self.browser.getControl("Save").click()

        self.assertEqual(
            "My Task",
            self.portal['my-task'].title,
        )

    def test_view_task(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory(
            "Task",
            id="my-task",
            title="My Task",
        )

        import transaction
        transaction.commit()

        self.browser.open(self.portal_url + '/my-task')

        self.assertTrue('My Task' in self.browser.contents)
