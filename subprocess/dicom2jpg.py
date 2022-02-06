#!/usr/bin/env python
# file: dicom2jpg.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2016-2021 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2016-02-13T10:51:55+01:00
# Last modified: 2022-02-06T13:46:27+0100
"""
Convert DICOM files from an X-ray machine to JPEG format.

This version manages a list of subprocesses itself.

During the conversion process, blank areas are removed. The blank area removal
is based on the image size of a Philips flat detector. The image goes from
2048x2048 pixels to 1574x2048 pixels.
"""

from datetime import datetime
from functools import partial
import argparse
import logging
import os
import subprocess as sp
import sys
import time

__version__ = "2022.02.06"


def main():
    """
    Entry point for dicom2jpg.
    """
    args = setup()
    if not args.fn:
        logging.error("no files to process")
        sys.exit(1)
    if args.quality != 80:
        logging.info(f"quality set to {args.quality}")
    if args.level:
        logging.info("applying level correction.")
    start_partial = partial(start_conversion, quality=args.quality, level=args.level)

    starttime = str(datetime.now())[:-7]
    logging.info(f"started at {starttime}.")
    # List of subprocesses
    procs = []
    # Do not launch more processes concurrently than your CPU has cores.
    # That will only lead to the processes fighting over CPU resources.
    maxprocs = os.cpu_count()
    # Launch and mange subprocesses for all files.
    for path in args.fn:
        while len(procs) == maxprocs:
            manageprocs(procs)
        procs.append(start_partial(path))
    # Wait for all subprocesses to finish.
    while len(procs) > 0:
        manageprocs(procs)
    endtime = str(datetime.now())[:-7]
    logging.info(f"completed at {endtime}.")


def setup():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--log",
        default="warning",
        choices=["debug", "info", "warning", "error"],
        help="logging level (defaults to 'warning')",
    )
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.add_argument(
        "-l",
        "--level",
        action="store_true",
        default=False,
        help="Correct color levels (default: no)",
    )
    parser.add_argument(
        "-q", "--quality", type=int, default=80, help="JPEG quailty level (default: 80)"
    )
    parser.add_argument(
        "fn", nargs="*", metavar="filename", help="DICOM files to process"
    )
    args = parser.parse_args(sys.argv[1:])
    logging.basicConfig(
        level=getattr(logging, args.log.upper(), None),
        format="%(levelname)s: %(message)s",
    )
    logging.debug(f"command line arguments = {sys.argv}")
    logging.debug(f"parsed arguments = {args}")
    # Check for requisites
    try:
        sp.run(["convert"], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
        logging.info("found “convert”")
    except FileNotFoundError:
        logging.error("the program “convert” cannot be found")
        sys.exit(1)
    return args


def start_conversion(filename, quality, level):
    """
    Convert a DICOM file to a JPEG file.

    Removing the blank areas from the Philips detector.

    Arguments:
        filename: name of the file to convert.
        quality: JPEG quality to apply
        level: Boolean to indicate whether level adustment should be done.
    Returns:
        Tuple of (input filename, output filename, subprocess.Popen)
    """
    outname = filename.strip() + ".jpg"
    size = "1574x2048"
    args = [
        "convert",
        filename,
        "-units",
        "PixelsPerInch",
        "-density",
        "300",
        "-depth",
        "8",
        "-crop",
        size + "+232+0",
        "-page",
        size + "+0+0",
        "-auto-gamma",
        "-quality",
        str(quality),
    ]
    if level:
        args += ["-level", "-35%,70%,0.5"]
    args.append(outname)
    proc = sp.Popen(args, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    return (filename, outname, proc)


def manageprocs(proclist):
    """Check a list of subprocesses for processes that have ended and
    remove them from the list.

    Arguments:
        proclist: List of tuples. The last item in the tuple must be
                  a subprocess.Popen object.
    """
    for item in proclist:
        filename, outname, proc = item
        if proc.poll() is not None:
            logging.info(f"conversion of “{filename}” to “{outname}” finished.")
            proclist.remove(item)
    # since manageprocs is called from a loop, keep CPU usage down.
    time.sleep(0.05)


if __name__ == "__main__":
    main()
