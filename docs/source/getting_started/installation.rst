.. _installation:

Installation
************

Following Sections provide overview on how to install the package.

.. contents:: Contents
   :backlinks: top
   :local:

Standard Installation
=====================

Use the following advice to install the standard / user version of this
package, once you have **at least one push** on your **main** and **develop**
branch (so the respective :ref:`release workflows <workflows_releases>` are
triggered).

Linux
-----

Install using a console with your virtual environment activated:

Latest Stable Version
^^^^^^^^^^^^^^^^^^^^^
.. code-block:: console

   $ pip install tessif-examples

Latest Development Version (potentially unstable)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   $ pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ tessif-examples

This installs the TestPyPI_ version of :code:`MY-PROJECT` while resolving the dependencies on PyPI_.


Development Installation
========================

1. Install Pyenv_ (only if not already present)
2. Install Poetry_ and Nox_ (only if not already present)
3. Clone the repo to a local directory (uses package name if square bracket
   part is omitted):

   .. code-block:: console

      $ git clone https://github.com/tZ3ma/tessif-examples [tessif-examples-develop]

4. Change to the new local repo folder and activate the desired
   `python versions`_ using pyenv:

   .. code-block:: console

      $ ccd strutils

      $ pyenv install 3.10.4 (adjust version to your needs)
      $ pyenv install 3.9.13 (optional)
      $ pyenv install 3.8.13 (optional)

      $ pyenv local 3.10.4 3.9.13 3.8.13 (activate those desired)

5. Install the package with development requirements:

   .. code:: console

      $ poetry install

6. Auto generate and activate a virtual environment where the installed package
   is installed:

   .. code:: console

      $ poetry shell

7. (Optional) Alternatively, you can now run an interactive Python session, or
   the command-line interface if your package supports it:

   .. code:: console

      $ poetry run python
      $ poetry run tessif-examples



.. _PyPI: https://pypi.org/
.. _TestPyPI: https://test.pypi.org/
.. _Poetry: https://python-poetry.org/
.. _Nox: https://nox.thea.codes/
.. _Pyenv: https://github.com/pyenv/pyenv
.. _official instructions: https://github.com/pyenv/pyenv/wiki/Common-build-problems
.. _kebab case: https://en.wiktionary.org/wiki/kebab_case
.. _python versions: https://www.python.org/downloads/
.. _Github: https://github.com/
.. _API-Token: https://pypi.org/help/#apitoken
.. _Codecov: https://about.codecov.io/
.. _Secret: https://docs.github.com/en/github-ae@latest/actions/security-guides/encrypted-secrets
.. _Codacy: https://docs.codacy.com/
.. _Codeclimate: https://codeclimate.com/
.. _Scrutinizer: https://scrutinizer-ci.com/
