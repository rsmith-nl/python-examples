#!/usr/bin/env python3
# file: nacl-decrypt.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2022 R.F. Smith <rsmith@xs4all.nl>
# SPDX-License-Identifier: MIT
# Created: 2022-02-06T20:01:32+0100
# Last modified: 2022-02-06T20:09:21+0100

import sys
import time
import base64

import nacl.secret
import nacl.utils

if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} encrypted decripted password")
    sys.exit(1)

key = base64.b64decode(sys.argv[3].encode('ascii'))
box = nacl.secret.SecretBox(key)
print(f"Decoding “{sys.argv[1]}” to “{sys.argv[2]}” with key “{sys.argv[3]}”.")

begin = time.time()
bp = time.process_time()
with open(sys.argv[1], "rb") as infile, open(sys.argv[2], "wb") as outfile:
    outfile.write(box.decrypt(infile.read()))
end = time.time()
ep = time.process_time()
dt = end - begin
dp = ep - bp
print(f"{dt:.2f} real, {dp:.2f} user+sys")
