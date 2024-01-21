#!/usr/bin/env python
# file: find-devices.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2022 R.F. Smith <rsmith@xs4all.nl>
# SPDX-License-Identifier: MIT
# Created: 2022-02-06T16:07:01+0100
# Last modified: 2022-02-06T16:24:24+0100
"""Simple script to find and list USB devices. It excludes hubs"""

import usb.core

if __name__ == "__main__":
    devs = (d for d in usb.core.find(find_all=True) if d.idVendor != 0)
    print("Vendor:Prodct Name")
    for d in devs:
        print(f'0x{d.idVendor:04X}:0x{d.idProduct:04X} "{d.product}"')
