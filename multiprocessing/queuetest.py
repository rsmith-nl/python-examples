#!/usr/bin/env python
# file: queuetest.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2017 R.F. Smith <rsmith@xs4all.nl>
# SPDX-License-Identifier: MIT
# Created: 2017-12-31T11:00:44+0100
# Last modified: 2022-02-05T22:26:00+0100
"""
How to use a multiprocessing.Queue.
Edited from my answer to https://stackoverflow.com/questions/48040696"""

import random
from multiprocessing import Process, Queue
import time
from datetime import datetime


def function1(q):
    while True:
        daydate = datetime.now()
        number = random.randrange(1, 215)
        print("Sent to function2: ({}, {})".format(daydate, number))
        q.put((daydate, number))
        time.sleep(2)


def function2(q):
    while True:
        date, number = q.get()
        print("Recevied values from function1: ({}, {})".format(date, number))
        time.sleep(2)


if __name__ == "__main__":
    q = Queue()
    a = Process(target=function1, args=(q,))
    a.start()
    b = Process(target=function2, args=(q,))
    b.start()
    a.join()
    b.join()
