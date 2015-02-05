==============================================================================
Part 1: Package Setup
==============================================================================

Create Package
==============

Create virtual Python environment::

  $ virtualenv-2.7 .env

Activate virtual Python environment::

  $ source .env/bin/activate

Install mr.bob with plone templates::

  $ pip install mr.bob bobtemplates.plone

Create a new 'plone_addon' package::

  $ mrbob -O plonetraining.testing bobtemplates:plone_addon


Buildout
========

Run buildout::

  $ cd plonetraining.testing
  $ python bootstrap-buildout.py --setuptools-version=8.3
  $ bin/buildout

Run tests::

  $ bin/test

Run all tests including robot tests::

  $ bin/test --all

