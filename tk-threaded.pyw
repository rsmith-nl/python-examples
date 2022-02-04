#!/usr/bin/env python
# file: tk-threaded.pyw
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2022 R.F. Smith <rsmith@xs4all.nl>
# SPDX-License-Identifier: MIT
# Created: 2022-02-02T21:40:48+0100
# Last modified: 2022-02-04T03:07:18+0100
"""Example tkinter script showing the use of a thread."""

import os
import sys
import threading
import time
import tkinter as tk
import tkinter.font as tkfont
import types

__version__ = "2022.02.02"
# Namespace for widgets that need to be accessed by callbacks.
widgets = types.SimpleNamespace()
# State that needs to be accessed by callbacks.
state = types.SimpleNamespace()


def create_widgets(root, w):
    """
    Create the window and its widgets.

    Arguments:
        root: the root window.
        w: SimpleNamespace to store widgets.
    """
    # General commands and bindings
    root.wm_title("tkinter threading v" + __version__)
    root.columnconfigure(2, weight=1)
    root.rowconfigure(3, weight=1)
    # First row
    tk.Label(root, text="Thread status: ").grid(row=0, column=0, sticky="ew")
    w.runstatus = tk.Label(root, text="not running", width=12)
    w.runstatus.grid(row=0, column=1, sticky="ew")
    # Second row
    tk.Label(root, text="Timer: ").grid(row=1, column=0, sticky="ew")
    w.counter = tk.Label(root, text="0 s")
    w.counter.grid(row=1, column=1, sticky="ew")
    # Third row
    w.gobtn = tk.Button(root, text="Go", command=do_start)
    w.gobtn.grid(row=2, column=0, sticky="ew")
    w.stopbtn = tk.Button(root, text="Stop", command=do_stop, state=tk.DISABLED)
    w.stopbtn.grid(row=2, column=1, sticky="ew")


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
    """
    Function that is run in a separate thread.

    This function *does* update tkinter widgets.  In Python 3, this should be
    safe if a tkinter is used that is built with threads.
    """
    # Initialization
    widgets.runstatus["text"] = "running"
    # Work
    while state.run:
        time.sleep(0.25)
        state.counter += 0.25
        widgets.counter["text"] = f"{state.counter:.2f} s"
    # Finalization
    state.counter = 0.0
    widgets.counter["text"] = f"{state.counter:g} s"
    widgets.runstatus["text"] = "not running"


def do_start():
    """Callback for the “Go” button"""
    widgets.gobtn["state"] = tk.DISABLED
    widgets.stopbtn["state"] = tk.NORMAL
    state.run = True
    state.worker = threading.Thread(target=worker)
    state.worker.start()


def do_stop():
    """Callback for the “Stop” button"""
    widgets.gobtn["state"] = tk.NORMAL
    widgets.stopbtn["state"] = tk.DISABLED
    state.run = False
    state.worker = None


# Main program starts here.
if __name__ == "__main__":
    # Detach from the command line on UNIX systems.
    if os.name == "posix":
        if os.fork():
            sys.exit()
    # Initialize global state
    initialize_state(state)
    # Create the GUI window.
    root = tk.Tk(None)
    if os.name == "posix":
        # Make a floating window even if using a tiling window manager.
        # This “-type” is unknown on ms-windows.
        root.attributes("-type", "dialog")
    # Set the font
    default_font = tkfont.nametofont("TkDefaultFont")
    default_font.configure(size=12)
    root.option_add("*Font", default_font)
    create_widgets(root, widgets)
    root.mainloop()
