#!/usr/bin/env python3
# file: tk-color.pyw
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2022 R.F. Smith <rsmith@xs4all.nl>
# SPDX-License-Identifier: MIT
# Created: 2022-02-02T23:48:00+0100
# Last modified: 2022-02-04T01:21:45+0100
"""Example tkinter script for choosing a color."""

from tkinter.font import nametofont
from types import SimpleNamespace
import os
import sys
import tkinter as tk

__version__ = "2022.01.28"
# Namespace for widgets that need to be accessed by callbacks.
widgets = SimpleNamespace()
# State that needs to be accessed by callbacks.
state = SimpleNamespace()


def create_widgets(root, w):
    """Create the window and its widgets.

    Arguments:
        root: the root window.
        w: SimpleNamespace where widgets can be added to.
    """
    # General commands and bindings
    root.wm_title("Tkinter Color v" + __version__)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=1)
    root.rowconfigure(3, weight=1)
    root.minsize(400, 100)
    # First row
    tk.Label(root, text="Red").grid(row=0, column=0, sticky="w")
    w.red = tk.Scale(
        root, from_=0, to=255, orient=tk.HORIZONTAL, length=255, command=do_red
    )
    w.red.grid(row=0, column=1, sticky="nsew")
    w.lf = tk.LabelFrame(root, text="preview")
    w.lf.grid(row=0, column=2, rowspan=3)
    w.show = tk.Frame(w.lf, width=100, height=100, bg="#000000")
    w.show.pack(padx=2, pady=2)
    # Second row
    tk.Label(root, text="Green").grid(row=1, column=0, sticky="w")
    w.green = tk.Scale(
        root, from_=0, to=255, orient=tk.HORIZONTAL, length=255, command=do_green
    )
    w.green.grid(row=1, column=1, sticky="ew")
    # Third row
    tk.Label(root, text="Blue").grid(row=2, column=0, sticky="w")
    w.blue = tk.Scale(
        root, from_=0, to=255, orient=tk.HORIZONTAL, length=255, command=do_blue
    )
    w.blue.grid(row=2, column=1, sticky="ew")
    # Last row
    w.b = tk.Button(root, text="Quit", command=do_exit)
    w.b.grid(row=3, column=0, sticky="w")


# Callbacks
def do_exit(arg=None):
    root.destroy()


def do_red(r):
    state.red = int(r)
    update_color()


def do_green(g):
    state.green = int(g)
    update_color()


def do_blue(b):
    state.blue = int(b)
    update_color()


# Helper functions
def update_color():
    value = f"#{state.red:02x}{state.green:02x}{state.blue:02x}"
    widgets.show["bg"] = value


# Main program starts here.
if __name__ == "__main__":
    # Detach from the command line on UNIX systems.
    if os.name == "posix":
        if os.fork():
            sys.exit()
    # Initialize global state
    state.red, state.green, state.blue = 0, 0, 0
    # Create the GUI window.
    root = tk.Tk(None)
    if os.name == "posix":
        # Make a floating window even if using a tiling window manager.
        # This “-type” is unknown on ms-windows.
        root.attributes("-type", "dialog")
    # Set the font
    default_font = nametofont("TkDefaultFont")
    default_font.configure(size=12)
    root.option_add("*Font", default_font)
    create_widgets(root, widgets)
    root.mainloop()
