#!/usr/bin/env python3
# file: treeview.pyw
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2018 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2018-05-06T18:37:55+0200
# Last modified: 2022-02-04T16:42:07+0100
"""Example tkinter script for using a treeview."""

import tkinter.font as tkfont
import os
import sys
import tkinter as tk
import tkinter.ttk as ttk

__version__ = "2022.02.03"

if __name__ == "__main__":
    # Detach from the command line on UNIX systems.
    if os.name == "posix":
        if os.fork():
            sys.exit()
    # create the UI.
    root = tk.Tk()
    root.wm_title("Tkinter treeview example v" + __version__)
    root.resizable(False, False)
    # Set the font
    default_font = tkfont.nametofont("TkDefaultFont")
    default_font.configure(size=12)
    root.option_add("*Font", default_font)
    # Create the treeview.
    tree = ttk.Treeview(root)
    tree["columns"] = ("one", "two")
    tree.column("one", width=100)
    tree.column("two", width=100)
    tree.heading("one", text="column A")
    tree.heading("two", text="column B")
    # Filling the tree:
    tree.insert("", 0, text="Line 1", values=("1A", "1b"))
    id2 = tree.insert("", 1, "dir2", text="Dir 2")
    tree.insert(id2, "end", "dir 2", text="sub dir 2", values=("2A", "2B"))
    # alternatively:
    tree.insert("", 3, "dir3", text="Dir 3")
    tree.insert("dir3", 3, text=" sub dir 3", values=("3A", " 3B"))
    tree.pack()
    # Run the program.
    root.mainloop()
