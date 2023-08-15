"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
name: ffcuesplit
description: a simple CDDA splitter
license: GNU GPLv3
author: Jazz
contacts: webmaster@codej.ru
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import os
import shlex

from subprocess import Popen, PIPE


def check_dep(dependency):
    for path in os.getenv('PATH').split(':'):
        dep_bin = os.path.join(path, dependency)
        if os.path.exists(dep_bin):
            return True


def detect_f_type(name):
    dep = check_dep('file')
    if not dep:
        raise OSError(f'`file` is not installed')
    cmd = shlex.split(f'file -b --mime-type "{name}"')
    with Popen(cmd, stdout=PIPE, stderr=PIPE) as p:
        result = p.communicate()
    if p.returncode:
        raise RuntimeError('something bad happened')
    return result[0].decode('utf-8').strip()
