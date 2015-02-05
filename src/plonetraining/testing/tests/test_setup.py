# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""
from plonetraining.testing.testing import PLONETRAINING_TESTING_INTEGRATION_TESTING  # noqa
from plone import api

import unittest2 as unittest


class TestInstall(unittest.TestCase):
    """Test installation of plonetraining.testing into Plone."""

    layer = PLONETRAINING_TESTING_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if plonetraining.testing is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('plonetraining.testing'))

    def test_uninstall(self):
        """Test if plonetraining.testing is cleanly uninstalled."""
        self.installer.uninstallProducts(['plonetraining.testing'])
        self.assertFalse(self.installer.isProductInstalled('plonetraining.testing'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IPlonetrainingTestingLayer is registered."""
        from plonetraining.testing.interfaces import IPlonetrainingTestingLayer
        from plone.browserlayer import utils
        self.assertIn(IPlonetrainingTestingLayer, utils.registered_layers())
