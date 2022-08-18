.. _installation:

Installation
************

Following Sections provide overview on how to install the package.

.. contents:: Contents
   :backlinks: top
   :local:


Using This Project Template
===========================

Use the following guide to fully take advantage of this project template:

1. Install Pyenv_ (only if not already present):

   A. Download and install using bash:

      .. code-block:: console

         $ curl https://pyenv.run | bash

   B. Add the following lines to your :file:`~/.bashrc` to make pyenv known to
      your system:

      .. code-block:: console

	 $ export PATH="~/.pyenv/bin:$PATH"
	 $ eval "$(pyenv init -)"
	 $ eval "$(pyenv virtualenv-init -)"

   C. Open a new shell, or :code:`source ~/.bashrc` in your current shell

   D. Install the Python build dependencies for your platform, using one of the
      commands listed in the `official instructions`_. For example, on a recent
      Ubuntu this would be:

      .. code-block:: console

	 $ sudo apt update && sudo apt install -y make build-essential libssl-dev zlib1g-dev \
	 $ libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
         $ libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

2. Create a new folder representing your repo/published package using `kebab case`_:

   .. code-block:: console

      $ mkdir my-project

3. Install the desired `python versions`_ using pyenv:

   .. code-block:: console

      $ pyenv install 3.10.4
      $ pyenv install 3.9.13
      $ pyenv install 3.8.13


4. Clone the `hpmpy-template` into your new local repo folder:

   .. code-block:: console

      $ git clone https://github.com/tZ3ma/tessif-examples my-project

5. Change into the new project folder and ctivate the desired `python versions`_

   .. code-block:: console

      $ cd my-project
      $ pyenv local 3.10.4 3.9.13 3.8.13


6. Install poetry (only if not already present)

   1. Download the poetry install script and run it

      .. code-block:: console

         $ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

   2. Open a new shell or :code:`source ~/.poetry/env` in your current shell


7. Install nox:

   .. code-block:: console

      $ pip install --user --upgrade nox

8. Rename all hpmpy instances after your project using git grep by replacing
   :code:`MY-PROJECT` below:

   .. code-block:: console

      $ git grep -lz tessif-examples | xargs -0 sed -i -e "s/tessif-examples/MY-PROJECT/g"
      $ git grep -lz tessif_examples | xargs -0 sed -i -e "s/tessif_examples/MY_PROJECT/g"

9. Rename the :file:`src/tessif_examples` package folder by replacing
   :code:`MY_PROJECT` below:

      .. code-block:: console

         $ mv src/tessif_examples src/MY_PROJECT

10. Install your package using poetry:

    .. code-block:: console

       $ poetry install

11. Run your first nox sessions:

    .. code-block:: console

       $ nox

12. Bump your package version to 0.1.0:

    .. code-block:: console

       $ poetry version minor

    Modify the `tests/test_version.py` file accordingly

13. Create a remote repo on Github_

14. Integrate your PyPI_  and TestPyPI_ API-Token_ as explained in the
    :ref:`release workflow <workflows_releases>` sections.

15. Add coverage reports using Codecov_:

    1. Go to the Codecov_ website and login using your Github_ account.

    2. Click on ``not yet setup`` and copy the API-Token in point 2.

    3. Make it a Secret_ in your remote repo called ``CODECOV_TOKEN``

    4. Your next push to the remote repo  will trigger the test workflow in
       :file:`.github/workflows/tests.yml` which will then automatically upload
       the coverage report to Codecov_

15. Install and add git pre-commit hooks:

    .. code-block:: console

       pip install --user --upgrade pre-commit
       pre-commit install

16. Add, commit and push all changes to your new remote repo:

    .. code-block:: console

       $ git add -A
       $ git commit -m "Project Initialization"
       $ git remote set-url origin https://github.com/GIT-USER/MY-PROJECT.git
       $ git branch -M main
       $ git push -u origin main

17. All set up! Now branch of your **main** branch to create the **develop**
    branch and add first implementations:

    A. Create switch to new develop branch:

       .. code-block:: console

          $ git checkout -b develop

    B. Modify the ``README.rst``, ``docs/index.rst`` and
       the ``docs/source/getting_started/installation.rst`` files to refelct
       your project description.

    C. Add sub-packages and/or modules to the ``src/strutils/`` folder

    D. Add, commit and push all changes/addition to your remote repo

       .. code-block:: console

          $ git add -A
	  $ git commit -m "Initial Implementation"
	  $ git push -u origin develop


18. (Optional) Create accounts on Codacy_, Codeclimate_ and Scrutinizer_ for
    code quality checks using you Github_ account.

19. All done! Make sure to checkout the
    :ref:`Workflows Developer Guide <workflows>` to acquaint yourself with the
    usage of Poetry_, Nox_ and Github_.






Development Install of Your Package Created with this Template
==============================================================

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

56 Auto generate and activate a virtual environment where the installed package
   is installed:

   .. code:: console

      $ poetry shell

7. (Optional) Alternatively, you can now run an interactive Python session, or
   the command-line interface if your package supports it:

   .. code:: console

      $ poetry run python
      $ poetry run tessif-examples


User Install of  Your Package Created with this Template
========================================================

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
