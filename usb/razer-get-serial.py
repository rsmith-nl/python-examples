#!/usr/bin/env python3
# file: razer-get-serial.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2020 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2020-03-18T20:45:17+0100
# Last modified: 2022-02-06T16:04:55+0100
"""Get the serial number from a Razer keyboard.

Tested on a BlackWidow Elite and an Ornata Chroma.
"""

import argparse
import logging
import struct
import sys
import usb.core

__version__ = "2022.02.06"


responses = {
    0x01: "busy",
    0x02: "command completed successfully",
    0x03: "command failed",
    0x04: "command timed out",
    0x05: "command not supported",
}


def serial_message():
    status = 0x00
    transaction_id = 0xFF
    remaining_packets = 0x00
    protocol_type = 0x00
    data_size = 0x16
    command_class = 0x00
    command_id = 0x82
    logging.debug(f"input msg: status = 0x{status:02x}")
    logging.debug(f"input msg: transaction_id = 0x{transaction_id:02x}")
    logging.debug(f"input msg: remaining_packets = 0x{remaining_packets:04x}")
    logging.debug(f"input msg: protocol_type = 0x{protocol_type:02x}")
    logging.debug(f"input msg: data_size = 0x{data_size:02x}")
    logging.debug(f"input msg: command_class = 0x{command_class:02x}")
    logging.debug(f"input msg: command_id = 0x{command_id:02x}")
    msg = struct.pack(
        ">BBHBBBB80x",
        status,
        transaction_id,
        protocol_type,
        remaining_packets,
        data_size,
        command_class,
        command_id,
    )
    chksum = 0
    for j in msg[2:]:  # Calculate the checksum
        chksum ^= j
    msg += bytes([chksum, 0])
    logging.debug(f"input msg: crc = 0x{chksum:02x}")
    return msg


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--log",
        default="warning",
        choices=["debug", "info", "warning", "error"],
        help="logging level (defaults to 'warning')",
    )
    parser.add_argument("-v", "--version", action="version", version=__version__)
    args = parser.parse_args(sys.argv[1:])
    logging.basicConfig(
        level=getattr(logging, args.log.upper(), None),
        format="%(levelname)s: %(message)s",
    )
    devs = list(usb.core.find(find_all=True, idVendor=0x1532))
    if devs:
        dev = devs[0]
    else:
        logging.warning("no Razer devices found; exiting.")
        sys.exit(1)
    # First request
    request_type = 0x21  # binary: 0 01 00001; host to device
    request = 0x09
    value = 0x300
    report_index = 0x01
    msg = serial_message()
    send = dev.ctrl_transfer(request_type, request, value, report_index, msg)
    logging.debug(
        f"ctrl_transfer(0x{request_type:02x}, 0x{request:02x}, "
        f"0x{value:02x}, 0x{report_index:02x}, ...) = {send}"
    )
    if send != 90:
        logging.error("first transfer failed.")
        sys.exit(2)
    logging.debug("Input command received correctly.")
    # Second request
    request_type = 0xA1  # binary 1 01 00001; device to host
    request = 0x01
    value = 0x300
    response_index = 0x01
    result = dev.ctrl_transfer(request_type, request, value, response_index, 90)
    logging.debug(
        f"ctrl_transfer(0x{request_type:02x}, 0x{request:02x}, "
        f"0x{value:02x}, 0x{response_index:02x}, ...) = {result}"
    )
    logging.debug(f"returned {len(result)} bytes.")
    if len(result) != 90:
        logging.error("second transfer failed.")
        sys.exit(3)
    (
        status,
        transaction_id,
        remaining_packets,
        protocol_type,
        data_size,
        command_class,
        command_id,
        arguments,
        crc,
    ) = struct.unpack(">BBHBBBB80sBx", result)
    logging.debug(f"result msg: status = 0x{status:02x}, <{responses[status]}>")
    logging.debug(f"result msg: transaction_id = 0x{transaction_id:02x}")
    logging.debug(f"result msg: remaining_packets = 0x{remaining_packets:04x}")
    logging.debug(f"result msg: protocol_type = 0x{protocol_type:02x}")
    logging.debug(f"result msg: data_size = 0x{data_size:02x}")
    logging.debug(f"result msg: command_class = 0x{command_class:02x}")
    logging.debug(f"result msg: command_id = 0x{command_id:02x}")
    logging.debug(f"result msg: arguments = {arguments[:data_size]}")
    logging.debug(f"result msg: crc = 0x{crc:02x}")
    serial = arguments.decode("ascii").strip()
    print(f"serial number: {serial}")
