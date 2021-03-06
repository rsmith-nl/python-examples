Python example programs
#######################

:tags: python
:author: Roland Smith

.. Last modified: 2022-02-14T23:25:48+0100
.. vim:spelllang=en

Introduction
============

This repository contains several example programs written in Python_ 3.
Some are based off answer I've given on stackoverflow_, others started as
small experiments for myself.

.. _Python: http://www.python.org/
.. _stackoverflow: https://stackoverflow.com/

Most of the programs have information about themselves in the docstring at the
beginning of the file, just after the header.

These programs are meant for me to remember and for others to learn from.
Given that there are a number of different programs in this repository,
releases or packages for this repo should not be expected.
Just clone the repo or download the zipfile from the ``main`` branch.


Requirements
============

Features used in these programs, such as f-strings means that *at least*
Python 3.6 is required to run them.
At the moment they've been confirmed to run on Python 3.9.

Programs that fit a certain theme are put in appropriate subdirectories, based
on modules that they require.

.. code-block:: console

    .
    ├── multiprocessing
    ├── nacl
    ├── subprocess
    ├── tkinter
    └── usb

The ``multiprocessing`` and ``subprocess`` modules are part of Python's
standard library.
The programs in the other directories require additional modules.

Since the ``tkinter`` module is an optional part of the CPython installation,
you have to make sure it is installed if you want to try those examples.
On ms-windows ``tkinter`` is part of the default install. When choosing a custom
installation, make sure that the “IDLE and tcl/tk” option is selected.
Some distributions for UNIX-like operating systems put ``tkinter`` in separate
packages. YMMV.

For the other modules, links to the Python Package Index are given below.

* ``nacl``: https://pypi.org/project/PyNaCl/
* ``usb``: https://pypi.org/project/pyusb/

Unfortunately, there are no recent binary packages for ms-windows for nacl
available, AFAICT.
The wheel for pyusb requires libusb 1.x, libusb 0.1.x or OpenUSB.
