====================================
ByteBlower Test Framework - Examples
====================================

This repository contains example scripts using the `ByteBlower Test Framework`_.

.. _ByteBlower Test Framework: https://pypi.org/project/byteblower-test-framework/.

Each directory describes a specific use case.

Please feel free to look around and grasp for your needs!

Usage
=====

#. Install Python (>= 3.7)
#. Create and initialize local Python virtual environment

   .. code-block:: console

      python3 -m venv --clear env

      . ./env/bin/activate

#. Update ``pip`` and ``build`` tools

   .. code-block:: console

      pip install -U pip build

#. Install dependencies

   .. code-block:: console

      pip install byteblower-test-framework

#. Run the test

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
