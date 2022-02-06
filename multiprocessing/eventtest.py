#!/usr/bin/env python
# file: eventtest.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2016 R.F. Smith <rsmith@xs4all.nl>
# SPDX-License-Identifier: MIT
# Created: 2016-05-04 23:52:36 +0200
# Last modified: 2022-02-05T23:58:33+0100
"""
Shows usate of multiprocessing.Event.
Edited from my answer to https://stackoverflow.com/questions/37015000.
"""
import multiprocessing as mp
import time


def worker(num, sw, sm):
    if num == 5:
        print("This is worker", num)
        time.sleep(1)
        print("Worker", num, "signalling main program to quit")
        sm.set()
    while not sw.is_set():
        print("This is worker", num)
        time.sleep(0.7)
    else:
        print("Worker", num, "signing off..")


if __name__ == "__main__":
    stop_worker = mp.Event()
    stop_main = mp.Event()

    workers = [
        mp.Process(target=worker, args=(n, stop_worker, stop_main)) for n in range(1, 6)
    ]
    for w in workers:
        w.start()
    while not stop_main.is_set():
        time.sleep(1)
    print("MAIN: Received stop event")
    print("MAIN: Sending stop event to workers")
    stop_worker.set()
    for c, w in enumerate(workers, start=1):
        w.join()
        print("worker", c, "joined")
