Lab 3 Notes
===========

Docstrings
----------

The project uses Python docstrings on modules, classes, and functions. They
are available through ``__doc__`` and ``help()`` and can be read by Sphinx.
Napoleon is enabled so the concise docstrings and parameter details are
converted into readable Sphinx documentation.


Documentation Coverage
----------------------

Sphinx autodoc directly imports the OOP, database, PyQt5, and Tkinter modules.
The Tkinter application only starts when ``main()`` is called, so its helpers
and callbacks are included in the generated API documentation without opening
the GUI during the build.

Sphinx Workflow
---------------

From the project folder, install the documentation dependency if needed:

.. code-block:: powershell

   python -m pip install -r docs\requirements.txt

Build the HTML documentation with:

.. code-block:: powershell

   sphinx-build -b html docs docs\_build\html

The generated site is available at ``docs\_build\html\index.html``.
To rebuild from scratch, remove the build directory or run:

.. code-block:: powershell

   sphinx-build -M clean docs docs\_build
   sphinx-build -b html docs docs\_build\html

Project Details
---------------

:Project: School Management System
:Author: Khaled Kanawati
:Version: 1.0.0
:Copyright: 2026, Khaled Kanawati
