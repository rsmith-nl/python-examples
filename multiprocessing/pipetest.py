#!/usr/bin/env python
# file: pipetest.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2020 R.F. Smith <rsmith@xs4all.nl>
# SPDX-License-Identifier: MIT
# Created: 2020-08-07T11:27:44+02:00
# Last modified: 2022-02-05T22:25:56+0100
"""
How to use a multiprocessing.Pipe.
From my answer to https://stackoverflow.com/questions/63294705
"""

from multiprocessing import Process, Pipe
import time


def worker(p):
    count = 0
    while True:
        count += 1
        val = "val" + str(count)
        p.send(val)
        print("worker sent:", val)
        time.sleep(0.5)


if __name__ == "__main__":
    child, parent = Pipe()

    p = Process(target=worker, args=(child,))
    p.daemon = True
    p.start()

    while True:
        if parent.poll():
            print("main received:", parent.recv())
        time.sleep(0.25)
