#!/usr/bin/env python3
# file: tk-stopwatch.pyw
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2020 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2020-04-16T22:14:50+0200
# Last modified: 2022-02-03T20:39:03+0100
"""Example tkinter script showing use of the “after” timeout."""

from tkinter.font import nametofont
import time
import tkinter as tk
import types

__version__ = "2022.02.03"


def start():
    state.starttime = time.time()
    state.run = True
    display()
    root.after(1000, update)


def stop():
    state.run = False
    state.starttime = None
    box.delete(0, tk.END)


def update():
    if state.run:
        display()
        root.after(1000, update)


def display():
    difference = int(time.time() - state.starttime)
    minutes, seconds = divmod(difference, 60)
    hours, minutes = divmod(minutes, 60)
    display = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    box.delete(0, tk.END)
    box.insert(0, display)


if __name__ == "__main__":
    # Create program state
    state = types.SimpleNamespace()
    state.starttime = None
    state.run = False
    # Create widgets.
    root = tk.Tk()
    root.title("Stopwatch v" + __version__)
    root.attributes("-type", "dialog")
    # Set the font
    default_font = nametofont("TkDefaultFont")
    default_font.configure(size=12)
    root.option_add("*Font", default_font)
    # box to display stopwatch
    box = tk.Entry(root, width=20, borderwidth=5)
    box.grid(row=0, column=0)
    start_button = tk.Button(root, text="Start", command=start)
    stop_button = tk.Button(root, text="Stop", command=stop)
    start_button.grid(row=1, column=0)
    stop_button.grid(row=2, column=0)
    # Run the GUI
    root.mainloop()