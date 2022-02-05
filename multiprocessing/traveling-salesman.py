#!/usr/bin/env python3
# file: traveling-salesman.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2020 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2020-04-09T00:15:58+0200
# Last modified: 2022-02-05T22:30:48+0100
"""A solution to the traveling salesman problem."""

import itertools as it
import multiprocessing as mp

# The worker function needs to access the cost matrix.
# So for this to work on ms-windows, it needs to be importable.
cost_matrix = [
    [0, 5, 7, 3, 2, 4, 6, 2, 1],
    [4, 0, 3, 6, 7, 2, 3, 4, 5],
    [6, 4, 0, 4, 9, 9, 9, 9, 9],
    [4, 5, 6, 0, 2, 3, 7, 8, 6],
    [1, 2, 3, 4, 0, 9, 8, 7, 6],
    [9, 8, 3, 4, 1, 0, 9, 8, 3],
    [1, 8, 9, 4, 2, 1, 0, 9, 8],
    [3, 2, 1, 9, 4, 1, 5, 0, 9],
    [1, 9, 8, 2, 3, 7, 4, 6, 0],
]


def worker(travel):
    cost = 0
    for start, end in zip(travel[:-1], travel[1:]):
        cost += cost_matrix[start][end]
    return cost, travel


if __name__ == "__main__":
    stops = tuple(range(len(cost_matrix[0])))
    travels = it.permutations(stops, len(stops))

    pl = mp.Pool()
    shortest = None
    saved_cost = 1e12
    count = 0
    for cost, travel in pl.imap_unordered(worker, travels):
        count += 1
        if cost < saved_cost:
            saved_cost = cost
            shortest = travel
            print("new shortest route:", count, travel, "cost =", cost)
    print(count, "routes evaluated.")
