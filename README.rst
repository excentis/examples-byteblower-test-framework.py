====================================
ByteBlower Test Framework - Examples
====================================

This repository contains example scripts using the `ByteBlower Test Framework`_.

.. _ByteBlower Test Framework: https://pypi.org/project/byteblower-test-framework/.

Each directory describes a specific use case.

Please feel free to look around and grasp for your needs!

Usage
=====

Python
------

The ByteBlower Test Framework currently supports Python version >= 3.7
and < 3.10 (due to incompatibility with one of its dependent packages).


Python virtual environment
--------------------------

Using Python ``venv`` (*included in Python >= 3.3*):

Prepare Python virtual environment: Create the virtual environment and install/update ``pip`` and ``build``.

.. note::
   _Mind the ``.`` which means **sourcing** ``./env/bin/activate``._

.. code-block:: console

   python3 -m venv --clear env
   . ./env/bin/activate
   pip install -U pip build

Install the ByteBlower Test Framework and its dependencies

.. code-block:: console

   . ./env/bin/activate
   pip install byteblower-test-framework

Run the test
------------

#. Go to the example subdirectory directory

   .. code-block:: console

      cd <example-subdir>

#. Make reports output directory

   .. code-block:: console

      mkdir reports

#. Run the test script

   .. code-block:: console

      python <example_test>.py

Development
===========

Create and initialize local Python virtual environment

.. code-block:: console

   python3 -m venv --clear env

   . ./env/bin/activate

   pip install -U pip build

   pip install byteblower-test-framework[dev,test,docs-dev]
