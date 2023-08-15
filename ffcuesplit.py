#!/usr/bin/env python3

"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
name: ffcuesplit
description: a simple CDDA splitter
license: GNU GPLv3
author: Jazz
contacts: webmaster@codej.ru
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from ffcuesplit import version
from ffcuesplit.main import parse_args, show_error, start_the_process

try:
     start_the_process(parse_args(version))
except Exception as e:
     show_error(e)
