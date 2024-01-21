#!/usr/bin/env python3
# file: nacl-encrypt.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2019 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2019-09-07T23:06:11+0200
# Last modified: 2022-02-06T20:09:40+0100

import sys
import time
import base64

import nacl.secret
import nacl.utils

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} input encrypted")
    sys.exit(1)

key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
box = nacl.secret.SecretBox(key)
kk = base64.b64encode(key).decode("ascii")
print(f"Encoding “{sys.argv[1]}” with key “{kk}”.")

begin = time.time()
bp = time.process_time()
with open(sys.argv[1], "rb") as infile, open(sys.argv[2], "wb") as outfile:
    outfile.write(box.encrypt(infile.read()))
end = time.time()
ep = time.process_time()
dt = end - begin
dp = ep - bp
print(f"{dt:.2f} real, {dp:.2f} user+sys")
