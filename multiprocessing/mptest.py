#!/usr/bin/env python
# file: mptest.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2019 R.F. Smith <rsmith@xs4all.nl>
# SPDX-License-Identifier: MIT
# Created: 2019-07-23T14:06:20+02:00
# Last modified: 2022-02-05T22:25:52+0100
"""Test IPC speed when returning data from a worker process."""

import multiprocessing as mp
import os
import time
import sys
import statistics


def worker(ident):
    data = os.urandom(SIZE)
    return ident, time.time(), data


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(f"Usage: {sys.argv[0]} n")
        print("Where “n” is memory size in MiB.")
        sys.exit(1)
    SIZE = int(sys.argv[1]) * 1024 * 1024  # data size in MiB. 400 eats all the RAM!
    COUNT = 10  # Number of workers

    print(f"SIZE = {SIZE} bytes")
    pool = mp.Pool()
    alltimes = []
    for ident, start, data in pool.imap_unordered(worker, list(range(COUNT))):
        dt = time.time() - start
        alltimes.append(dt)
        del data
        print(f"Received data from #{ident}, took {dt:.3f} s to transfer.")
    avgspeed = SIZE / statistics.mean(alltimes) / 1e6  # MB/s
    print(f"Average transfer speed: {avgspeed:.0f} MB/s")
