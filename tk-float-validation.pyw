#!/usr/bin/env python
# file: tk-floatentry.pyw
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2022 R.F. Smith <rsmith@xs4all.nl>
# SPDX-License-Identifier: MIT
# Created: 2022-02-03T00:45:38+0100
# Last modified: 2022-02-03T20:33:12+0100
"""Example tkinter script to show input validation."""

from tkinter.font import nametofont
from types import SimpleNamespace
import os
import sys
import tkinter as tk

__version__ = "2022.02.03"
# Namespace for widgets that need to be accessed by callbacks.
widgets = SimpleNamespace()


def create_widgets(root, w):
    """Create the window and its widgets.

    Arguments:
        root: the root window.
        w: SimpleNamespace where widgets can be added to.
    """
    # Set the font
    default_font = nametofont("TkDefaultFont")
    default_font.configure(size=12)
    root.option_add("*Font", default_font)
    # General commands and bindings
    root.wm_title("Tkinter float entry v" + __version__)
    # Create widgets
    w.qedit = tk.Entry(root, justify="right")
    w.qedit.insert(0, "100")
    w.qedit.grid(row=0, column=0, sticky="ew")
    w.result = tk.Label(root, text="100")
    w.result.grid(row=1, column=0)
    tk.Button(root, text="Exit", command=root.quit).grid(row=2, column=0)
    # Set up validation.
    vcmd = root.register(is_number)
    w.qedit["validate"] = "key"
    w.qedit["validatecommand"] = (vcmd, "%P")
    w.result.bind("<<UpdateNeeded>>", do_update)


def is_number(data):
    if data == "":
        return True
    try:
        float(data)
    except ValueError:
        if data.endswith(("e", "e-", "e+", "E", "E-", "E+")) or data in ("+", "-", "."):
            return True
        return False
    widgets.result.event_generate("<<UpdateNeeded>>", when="tail")
    return True


def do_update(event):
    w = event.widget
    number = float(widgets.qedit.get())
    w["text"] = f"{number}"


# Main program starts here.
if __name__ == "__main__":
    # Detach from the command line on UNIX systems.
    if os.name == "posix":
        if os.fork():
            sys.exit()
    # Create the GUI window.
    root = tk.Tk(None)
    if os.name == "posix":
        # Make a floating window even if using a tiling window manager.
        # This “-type” is unknown on ms-windows.
        root.attributes("-type", "dialog")
    create_widgets(root, widgets)
    root.mainloop()
