==============================================================================
Part 2: Plone Testing Setup
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

6) tearDownPloneSite(self, portal)

7) tearDownZope(self, app)


tests/test_setup.py
-------------------

.. literalinclude:: ../../src/plonetraining/testing/tests/test_setup.py
   :language: python
