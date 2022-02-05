#!/usr/bin/env python
# file: queuetest2.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2020 R.F. Smith <rsmith@xs4all.nl>
# SPDX-License-Identifier: MIT
# Created: 2020-08-07T11:27:44+02:00
# Last modified: 2022-02-05T22:26:05+0100
"""
How to use a multiprocessing.Queue.
Edited from my answer to https://stackoverflow.com/questions/63294705.
Simplified by using this process as well.
"""
from multiprocessing import Process, Queue
import time


def worker(q):
    count = 0
    while True:
        count += 1
        val = "val" + str(count)
        q.put(val)
        print("worker sent:", val)
        time.sleep(2)


if __name__ == "__main__":
    q = Queue()

    p = Process(target=worker, args=(q,))
    p.daemon = True
    p.start()

    while True:
        if not q.empty():
            print("main received:", q.get())
        time.sleep(1)
