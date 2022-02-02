#!/usr/bin/env python
# file: tkinter-threaded.pyw
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2022 R.F. Smith <rsmith@xs4all.nl>
# SPDX-License-Identifier: MIT
# Created: 2022-02-02T21:40:48+0100
# Last modified: 2022-02-02T22:18:47+0100

from types import SimpleNamespace
import os
import sys
import threading
import time
import tkinter as tk

__version__ = "2022.02.02"
widgets = SimpleNamespace()
state = SimpleNamespace()


def create_widgets(root, w):
    """
    Create the window and its widgets.

        Arguments:
        root: the root window.
        w: SimpleNamespace to store widgets.
    """
    # General commands and bindings
    root.wm_title('tkinter threading v' + __version__)
    root.columnconfigure(2, weight=1)
    root.rowconfigure(3, weight=1)
    # First row
    tk.Label(root, text='Thread status: ').grid(row=0, column=0, sticky='ew')
    w.runstatus = tk.Label(root, text='not running', width=12)
    w.runstatus.grid(row=0, column=1, sticky='ew')
    # Second row
    tk.Label(root, text='Timer: ').grid(row=1, column=0, sticky='ew')
    w.counter = tk.Label(root, text='0 s')
    w.counter.grid(row=1, column=1, sticky='ew')
    # Third row
    w.gobtn = tk.Button(root, text="Go", command=do_start)
    w.gobtn.grid(row=2, column=0, sticky='ew')
    w.stopbtn = tk.Button(root, text="Stop", command=do_stop, state=tk.DISABLED)
    w.stopbtn.grid(row=2, column=1, sticky='ew')


def initialize_state(s):
    """
    Initialize the global state.

    Arguments:
        s: SimpleNamespace to store application state.
    """
    s.worker = None
    s.run = False
    s.counter = 0


def worker():
    # Initialization
    widgets.runstatus['text'] = "running"
    # Work
    while state.run:
        time.sleep(0.25)
        state.counter += 0.25
        widgets.counter['text'] = f"{state.counter:.2f} s"
    # Finalization
    state.counter = 0.0
    widgets.counter['text'] = f"{state.counter:g} s"
    widgets.runstatus['text'] = "not running"


def do_start():
    """Callback for the “Go” button"""
    widgets.gobtn["state"] = tk.DISABLED
    widgets.stopbtn["state"] = tk.NORMAL
    state.run = True
    state.worker = threading.Thread(target=worker)
    state.worker.start()


def do_stop():
    """Callback for the “stop” button"""
    widgets.gobtn["state"] = tk.NORMAL
    widgets.stopbtn["state"] = tk.DISABLED
    state.run = False
    state.worker = None


if __name__ == '__main__':
    # Detach from the command line on UNIX systems.
    if os.name == 'posix':
        if os.fork():
            sys.exit()
    # Create the GUI window.
    root = tk.Tk(None)
    # Use a dialog window so that it floats even when using a tiling window manager.
    if os.name == 'posix':
        root.attributes('-type', 'dialog')
    create_widgets(root, widgets)
    initialize_state(state)
    root.mainloop()
