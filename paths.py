#!/usr/bin/env python
# file: paths.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2022 R.F. Smith <rsmith@xs4all.nl>
# Created: 2022-02-05T12:13:20+0100
# Last modified: 2022-02-07T09:18:11+0100
"""Print the “scripts” and “data” paths for the “_home” and “_user” schemes."""
import sysconfig as sc
import os

for scheme in (nm for nm in sc.get_scheme_names() if os.name in nm):
    print(f"{scheme}:")
    for path in ("scripts", "data"):
        print(f"* {path}:", sc.get_path(path, scheme))
