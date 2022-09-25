# file: logging-syslog.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2019 R.F. Smith <rsmith@xs4all.nl>
# Created: 2019-07-16T21:12:41+0200
# Last modified: 2022-02-05T19:42:42+0100
"""
Logging to syslog on a *BSD system.

See also: ~/WWW/src/programming/python-syslog.rst
"""
import os
import logging
import logging.handlers

# Toegevoegd aan syslog.conf;
# local3.*    /var/log/user.log
#
# Created the logfile:
# # touch /var/log/user.log
# # chmod 644 /var/log/user.log

# 19=LOG_LOCAL3, as per /usr/local/lib/python3.7/logging/handlers.py
syslog = logging.handlers.SysLogHandler(address="/var/run/log", facility=19)
pid = os.getpid()
syslog.ident = f"logging-syslog.py[{pid}]: "
logging.basicConfig(
    level="INFO", format="%(levelname)s: %(message)s", handlers=(syslog,)
)

# Test
logging.info("info level")  # werkt
logging.warning("warning level")  # werkt
logging.error("error level")  # werkt
