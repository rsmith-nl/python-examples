#!/usr/bin/env python
# file: embed.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2019 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2019-08-02T15:49:18+0200
# Last modified: 2022-02-06T17:28:49+0100
"""
Script to generate code to embed a file in a Python program.
The contents of the file are base85 encoded and written out as Python code.
Once the code is loaded, it returns the contents of the original file.

The py-include program from my scripts repo is an enhanced version.
"""

import base64
import os
import sys


def embed(path, name, linelen=75):
    """
    Returns python code to embed a binary file.

    Arguments:
        path (str): path of the file to encode.
        name (str): variable name that should be used for the file.

    Returns:
        Code to embed the file in b85 encoded format.

    Example:
    >>> from embed import embed
    >>> import base64, os
    >>> exec(embed('/usr/local/share/icons/Adwaita/16x16/apps/web-browser.png', 'wb'))
    >>> len(wb)
    892
    >>> wb[:4]
    b'\x89PNG'
    """
    with open(path, "rb") as df:
        data = base64.b85encode(df.read()).decode("ascii")
    lines = [f"{name} = base64.b85decode("]
    i = 0
    while i < len(data):
        lines.append("    \"" + data[i : i + linelen] + "\"")
        i += linelen
    lines.append(")")
    return os.linesep.join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} filename ...")
        sys.exit(1)
    filename = sys.argv[1]
    for filename in sys.argv[1:]:
        varname = os.path.splitext(os.path.basename(filename))[0]
        varname = varname.lower().replace("-", "_")
        print(f"\n# {filename}")
        print(embed(filename, varname))
