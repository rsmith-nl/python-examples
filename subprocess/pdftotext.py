# file: pdftotext.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2016 R.F. Smith <rsmith@xs4all.nl>
# SPDX-License-Identifier: MIT
# Created: 2016-04-03 16:41:34 +0200
# Last modified: 2022-02-05T23:51:15+0100
"""
Extract text from PDF files.

Based on my aswer to https://stackoverflow.com/questions/36337463.

Requires pdftotext from the poppler utilities.
On unix/linux install them using your favorite package manager.

Binaries for ms-windows can be found at;
1) http://blog.alivate.com.au/poppler-windows/
2) https://sourceforge.net/projects/poppler-win32/
"""

import subprocess


def pdftotext(pdf, page=None):
    """Retrieve all text from a PDF file.

    Arguments:
        pdf Path of the file to read.
        page: Number of the page to read, 2-tuple of (start,end) pages or None.
           If None, read all the pages.

    Returns:
        A list of lines of text.
    """
    if page is None:
        args = ["pdftotext", "-layout", "-q", pdf, "-"]
    else:
        if isinstance(page, int):
            args = [
                "pdftotext",
                "-f",
                str(page),
                "-l",
                str(page),
                "-layout",
                "-q",
                pdf,
                "-",
            ]
        elif isinstance(page, tuple) and len(page) == 2:
            args = [
                "pdftotext",
                "-f",
                str(min(page)),
                "-l",
                str(max(page)),
                "-layout",
                "-q",
                pdf,
                "-",
            ]
        else:
            raise ValueError("page must be int, 2-tuple or None")
    try:
        txt = subprocess.check_output(args, universal_newlines=True)
        lines = txt.splitlines()
    except subprocess.CalledProcessError:
        lines = []
    return lines
