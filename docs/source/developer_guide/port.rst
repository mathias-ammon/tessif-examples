.. _port:

Porting Old Examples
********************

Following sections provide information on how to port the old private repo
examples to this new library. It uses shell-commands_ which are denoted the
indented box as in::

  shell-command example

.. contents:: Contents
   :backlinks: top
   :local:


Preparation
===========

Shell Commands
--------------

When on windows, get access to a command executing shell_. Recommended
are:

- Python IDEs like PyCharm_
- Using the Windows-Powershell7_

  - (Usefull bash vs powershell-commands_ cheat sheet)

Old Repository
--------------

1. Get access to to the Old-Repo_
2. Clone the repo to your local machine using git_::

     git clone https://collaborating.tuhh.de/ietma/tessif.git

3. Locate the old files at::

     tessif/src/tessif/examples/data/tsf/py_hard.py

New Repository
--------------

1. Create a Github_ account
2. Clone the repo to your local machine using git_::

     git clone https://github.com/tZ3ma/tessif-examples.git

3. Navigate insdie the tessif-examples folder::

     cd tessif-examples

4. Create a new local `branch <Branches>`_ using git_::

     git checkout -b my-new-branch

5. Locate the locations at::

     tessif-examples/src/tessif-examples/

Doing the port
==============

Copy
----

1. Each of the functions in
   :file:`tessif/src/tessif/examples/data/tsf/py_hard.py` represent one
   singular energy system example and should be copied to its own
   ``.py - file`` in :file:`tessif-examples/src/tessif-examples/`. Either
   inside the ``basic`` folder or the ``scenarios`` folder. The filename
   should be called like the function, without ``create``.

2. ``basic`` examples are:

   - create_mwe
   - create_fpwe
   - emission_objective
   - create_connected_es
   - create_chp
   - create_variable_chp
   - create_storage_example
   - create_expansion_plan_example
   - create_simple_transformer_grid_es
   - create_time_varying_efficiency_transformer

3. ``scenarios`` examples are:

   - create_hhes
   - create_grid_es
   - create_component_es
   - create_grid_kp_es
   - create_grid_cs_es
   - create_grid_cp_es
   - create_grid_ts_es
   - create_grid_tp_es

Modify
------

1. Make sure each new function starts with ``create_``
2. Delete the ``"store on disk"`` part (see the already-ported-examples_ for
   more details):

   1. From the function arguments
   2. From the function docstring
   3. From the function body

3. Change the examples section:

   1. Only include the visualization
   2. Change the code snippet from docctest-style (``>>>`` and ``...``)
      to a standard code as seen in the already-ported-examples_
   3. Change the acutal code to use ``dcgraph`` instead of ``nxgraph`` as
      seen in the already-ported-examples_
   4. Store the system graph image at::

	tessif-examples/docs/source/_static/system_model_graphs/

   5. Change the source file linking to:

      ``.. image:: ../../_static/system_model_graphs/``

Add documentation
-----------------

1. Copy one of the existing ``.rst - files``, (e.g.
   :file:`tessif-examples/docs/source/examples/basic/mwe.rst`) according to
   the example your porting, so for ``create_chp`` this would be::

     tessif-examples/docs/source/examples/basic/chp.rst

2. Link the newly created ``.rst - files`` so the docs builder can include
   it. Linking the file is done by adding the relative path to the
   :file:`tessif-examples/docs/source/examples.rst` file.

   For the ``create_chp`` example this would result in adding following
   line::

     examples/basic/chp

Add tests
---------
1. Add a test function for your newly ported example inside
   :file:`tessif-examples/tests/examples/`) according to
   the example your porting. So for ``create_chp`` this would be an additional
   function called ``test_chp`` inside::

     tessif-examples/tests/examples/test_basic.py



.. _shell: https://saultcollege.github.io/shell-basics/
.. _shell-commands: https://www.tutorialspoint.com/what-are-shell-commands
.. _Windows-Powershell7: https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.2
.. _powershell-commands: https://mathieubuisson.github.io/powershell-linux-bash/

.. _git: https://git-scm.com/
.. _Github: https://github.com/
.. _Branches: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches
.. _Old-Repo: https://collaborating.tuhh.de/ietma/tessif


.. _PyCharm: https://www.jetbrains.com/pycharm/

.. _already-ported-examples: https://tessif-examples.readthedocs.io/en/latest/source/examples.html
