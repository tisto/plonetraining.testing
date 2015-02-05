# -*- coding: utf-8 -*-
"""Base module for unittesting."""

from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from zope.configuration import xmlconfig

import plonetraining.testing


class PlonetrainingTestingLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        print('\n ---> setUpZope \n')
        xmlconfig.file(
            'configure.zcml',
            plonetraining.testing,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        print('\n ---> setUpPloneSite \n')
        applyProfile(portal, 'plonetraining.testing:default')

    def tearDownZope(self, app):
        print('\n ---> tearDownZope \n')

    def tearDownPloneSite(self, portal):
        print('\n ---> tearDownPloneSite \n')


PLONETRAINING_TESTING_FIXTURE = PlonetrainingTestingLayer()

PLONETRAINING_TESTING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONETRAINING_TESTING_FIXTURE,),
    name='PlonetrainingTestingLayer:IntegrationTesting'
)

PLONETRAINING_TESTING_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONETRAINING_TESTING_FIXTURE,),
    name='PlonetrainingTestingLayer:FunctionalTesting'
)

PLONETRAINING_TESTING_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PLONETRAINING_TESTING_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='PlonetrainingTestingLayer:AcceptanceTesting'
)
