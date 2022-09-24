#!/usr/bin/env python3
# file: tk-stopwatch.pyw
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2020 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2020-04-16T22:14:50+0200
# Last modified: 2022-09-24T11:20:04+0200
"""Example tkinter script showing use of the “after” timeout."""

import os
import sys
import time
import tkinter as tk
import tkinter.font as tkfont
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
    # Detach from the command line on UNIX systems.
    if os.name == "posix":
        if os.fork():
            sys.exit()
    # Create program state
    state = types.SimpleNamespace()
    state.starttime = None
    state.run = False
    # Create widgets.
    root = tk.Tk()
    root.title("Stopwatch v" + __version__)
    root.resizable(False, False)
    # Set the font
    default_font = tkfont.nametofont("TkDefaultFont")
    default_font.configure(size=12)
    root.option_add("*Font", default_font)
    # box to display stopwatch
    box = tk.Entry(root, width=20, borderwidth=5, takefocus=0)
    box.grid(row=0, column=0, columnspan=3)
    start_button = tk.Button(root, text="Start", command=start)
    stop_button = tk.Button(root, text="Stop", command=stop)
    quit_button = tk.Button(root, text="Quit", command=root.quit)
    start_button.grid(row=1, column=0)
    stop_button.grid(row=1, column=1)
    quit_button.grid(row=1, column=2)
    # Run the GUI
    root.mainloop()
