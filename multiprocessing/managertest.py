#!/usr/bin/env python
# file: managertest.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2017 R.F. Smith <rsmith@xs4all.nl>
# Created: 2017-12-31 10:46:38 +0100
# Last modified: 2022-02-05T22:25:45+0100
"""
Shows usage of a multiprocessing.Manager.
Edited from my answer to https://stackoverflow.com/questions/48040696.
"""

import random
from multiprocessing import Process, Manager
import time
from datetime import datetime


def function1(d):
    while True:
        daydate = datetime.now()
        number = random.randrange(1, 215)
        print("Sent to function2: ({}, {})".format(daydate, number))
        d["date"] = daydate
        d["number"] = number
        time.sleep(2)


def function2(d):
    while True:
        print("Recevied values from function1: ({}, {})".format(d["date"], d["number"]))
        time.sleep(2)


if __name__ == "__main__":
    with Manager() as manager:
        d = manager.dict()
        a = Process(target=function1, args=(d,))
        a.start()
        b = Process(target=function2, args=(d,))
        b.start()
        a.join()
        b.join()
