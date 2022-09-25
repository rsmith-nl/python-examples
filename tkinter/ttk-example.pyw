#!/usr/bin/env python3
# file: ttk-example.pyw
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2018 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2018-05-06T18:37:55+0200
# Last modified: 2022-09-25T09:05:19+0200

import os
import sys

import tkinter as tk
from tkinter import ttk


def calculate(*args):
    try:
        value = float(feet.get())
        vstr = '{:.3f}'.format((0.3048 * value * 10000 + 0.5) / 10000)
        meters.set(vstr)
    except ValueError:
        pass


def quit(event):
    root.quit()


if __name__ == '__main__':
    # Detach from the command line on UNIX systems.
    if os.name == 'posix':
        if os.fork():
            sys.exit()

    # Create the GUI and run it.
    root = tk.Tk()
    root.attributes('-type', 'dialog')
    root.title("Feet to Meters")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    feet = tk.StringVar()
    meters = tk.StringVar()

    feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
    feet_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))
    feet_entry.bind('q', quit)

    ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(tk.W, tk.E))

    s = ttk.Style()
    s.configure('my.TButton', font=('Times', 12))
    calc = ttk.Button(mainframe, text="Calculate", command=calculate, style='my.TButton')
    calc.grid(column=3, row=3, sticky=tk.W)
    calc.bind('q', quit)

    ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=tk.W)
    ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=tk.E)
    ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=tk.W)

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    feet_entry.focus()
    root.bind('<Return>', calculate)

    root.mainloop()
