==============================================================================
Part 2: plone.app.testing Basics
==============================================================================

testing.py
----------

.. literalinclude:: ../../src/plonetraining/testing/testing.py
   :language: python


Testing Layers
--------------

1) testing.py: setUpZope(self, app, configurationContext)

2) testing.py: setUpPloneSite(self, portal)

3) test_setup.py: setUp

4) test_setup.py: test_product_installed

5) test_setup.py: tearDown

6) tearDownZope(self, app)

7) tearDownPloneSite(self, portal)


tests/test_setup.py
-------------------

.. literalinclude:: ../../src/plonetraining/testing/tests/test_setup.py
   :language: python
