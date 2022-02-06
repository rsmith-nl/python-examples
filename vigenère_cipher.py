#!/usr/bin/env python
# file: vigenère_cipher.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2022 R.F. Smith <rsmith@xs4all.nl>
# SPDX-License-Identifier: MIT
# Created: 2016-04-22T00:34:35+0200
# Last modified: 2022-02-06T00:06:24+0100
"""
Vigenère encryption.
Adapted from my answer to https://stackoverflow.com/questions/36780703.
"""

plaintext = "THISISAPLAINTEXT"
print(f"plaintext = {plaintext}")
key = "SPAMEGGS"
print(f"key = {key}")
count = int(len(plaintext) / len(key)) + 1

stretchedkey = [ord(c) for c in key * count]

# Encryption
plainnum = [ord(c) for c in plaintext]
ciphernum = [a + b - 65 for a, b in zip(plainnum, stretchedkey)]
ciphertext = "".join([chr(c) if c <= 90 else chr(c - 26) for c in ciphernum])
print(f"ciphertext = {ciphertext}")

# Decryption
ciphernum = [ord(c) for c in ciphertext]
decryptnum = [a - b + 65 for a, b in zip(ciphernum, stretchedkey)]
decrypted = "".join([chr(c) if c >= 65 else chr(c + 26) for c in decryptnum])
print(f"decrypted = {decrypted}")
