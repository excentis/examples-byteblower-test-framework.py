************************************
ByteBlower Test Framework - Examples
************************************

This repository contains example scripts
using the `ByteBlower Test Framework`_.

.. _ByteBlower Test Framework: https://pypi.org/project/byteblower-test-framework/.

Each directory describes a specific use case.

Please feel free to look around and grasp for your needs!

Usage
=====

Python requirements
-------------------

The ByteBlower Test Framework currently supports Python version 3.7 up to 3.11.

Python virtual environment
--------------------------

1. On Unix-based systems (Linux, WSL, macOS):

   Prepare Python virtual environment: Create the virtual environment
   and install/update ``pip`` and ``build``.

   **Note**:
   *Mind the leading* ``.`` *which means* **sourcing** ``./env/bin/activate``.

   .. code-block:: shell

      python3 -m venv --clear env
      . ./env/bin/activate
      pip install -U pip build

   Install the ByteBlower Test Framework and its dependencies

   .. code-block:: shell

      . ./env/bin/activate
      pip install byteblower-test-framework

2. On Windows systems using PowerShell:

      **Note**: On Microsoft Windows, it may be required to enable the
      Activate.ps1 script by setting the execution policy for the user.
      You can do this by issuing the following PowerShell command:

      .. code-block:: shell

         PS C:> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

      See `About Execution Policies`_ for more information.

   Prepare Python virtual environment: Create the virtual environment
   and install/update ``pip`` and ``build``.

   .. code-block:: shell

      python3.8.exe -m venv --clear env
      & ".\env\Scripts\activate.ps1"
      python3.8.exe -m pip install -U pip build

   Install the ByteBlower Test Framework and its dependencies

   .. code-block:: shell

      & ".\env\Scripts\activate.ps1"
      pip install byteblower-test-framework

.. _About Execution Policies: https://go.microsoft.com/fwlink/?LinkID=135170

Run the test
------------

#. Go to the example subdirectory directory

   .. code-block:: shell

      cd <example-subdir>

#. Make reports output directory

   .. code-block:: shell

      mkdir reports

#. Run the test script

   .. code-block:: shell

      python <example_test>.py

Development
===========

Create and initialize local Python virtual environment

1. On Unix-based systems (Linux, WSL, macOS):

   Prepare Python virtual environment: Create the virtual environment
   and install/update ``pip`` and ``build``.

   **Note**:
   *Mind the leading* ``.`` *which means* **sourcing** ``./env/bin/activate``.

   .. code-block:: shell

      python3 -m venv --clear env
      . ./env/bin/activate
      pip install -U pip build

   Install the ByteBlower Test Framework and its dependencies,
   including development requirements.

   .. code-block:: shell

      pip install byteblower-test-framework[dev,test,docs-dev]

2. On Windows systems using PowerShell:

   Prepare Python virtual environment: Create the virtual environment
   and install/update ``pip`` and ``build``.

      **Note**: On Microsoft Windows, it may be required to enable the
      Activate.ps1 script by setting the execution policy for the user.
      You can do this by issuing the following PowerShell command:

      .. code-block:: shell

         PS C:> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

      See `About Execution Policies`_ for more information.

   .. code-block:: shell

      python3.8.exe -m venv --clear env
      & ".\env\Scripts\activate.ps1"
      python3.8.exe -m pip install -U pip build

   Install the ByteBlower Test Framework and its dependencies,
   including development requirements.

   .. code-block:: shell

      pip install byteblower-test-framework[dev,test,docs-dev]
