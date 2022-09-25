# file: gnuplot.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2018 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2018-12-08T20:22:50+0100
# Last modified: 2018-12-15T14:02:40+0100
"""Example how to use gnuplot from Python."""

import subprocess as sp
import statistics as stat

title = "Title"
outputpath = "gnuplot.pdf"
xlabel = "sample"
ylabel = "variable [unit]"
datatitle = "variable"
yrangelabel = "moving range [unit]"

data = [
    1327,
    1324,
    1318,
    1325,
    1324,
    1323,
    1319,
    1319,
    1323,
    1315,
    1317,
    1316,
    1316,
    1314,
    1312,
    1316,
    1310,
    1309,
    1301,
    1310,
    1309,
    1307,
    1312,
    1304,
    1306,
    1309,
    1311,
    1307,
    1301,
    1299,
    1294,
    1290,
]
mean = stat.mean(data)
mr = [abs(a - b) for a, b in zip(data[1:], data[:-1])]
uclmr = 3.67 * stat.mean(mr)
offs = 2.66 * stat.mean(mr)
lcl = mean - offs
ucl = mean + offs

lines = [
    'set terminal pdfcairo enhanced color dashed font "Alegreya, 14" '
    "rounded size 16 cm, 12 cm",
    "set encoding utf8",
    f'set title "{title}"',
    f'set output "{outputpath}"',
    "set multiplot layout 2,1 downwards margins char 12,3,4,2 spacing char 3",
    f'set ylabel "{ylabel}"',
    "set key right top opaque",
    "$data <<EOD",
]
lines += [f"1 {data[0]}"]
lines += [f"{n} {m} {z}" for n, (m, z) in enumerate(zip(data[1:], mr), start=2)]
lines += [
    "EOD",
    f"lcl(x) = {lcl}",
    f"ucl(x) = {ucl}",
    f"uclmr(x) = {uclmr}",
    'plot ucl(x) with lines ls 2 dt 2 title "UCL", '  # Plot should be a single line!
    f'$data using 1:2 with linespoints ls 1 title "{datatitle}", '  # here as well
    'lcl(x) with lines ls 3 dt 3 title "LCL"',
    f'set ylabel "{yrangelabel}"',
    "unset title",
    f'set xlabel "{xlabel}"',
    'plot uclmr(x) with lines ls 2 dt 2 title "UCL", '
    '$data using 1:3 with linespoints ls 1 title "moving range"',
]
cp = sp.run(["gnuplot"], input="\n".join(lines).encode("utf-8"))
exit(cp.returncode)
