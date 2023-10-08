#!/usr/bin/python3
# Fabfile to delete out-of-date archives.
import os
from fabric.api import *

env.hosts = ["107.23.95.21", "34.204.81.3"]


def do_clean(number=0):
    """Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.

    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    number = int(number)
    with lcd("./versions"):
        if number > 1:
            local("ls -t | tail -n +{} | xargs rm -f".format(number + 1))
        else:
            local("ls -t | tail -n +2 | xargs rm -f")
    with cd("/data/web_static/releases"):
        if number > 1:
            run("ls -t | tail -n +{} | xargs rm -rf".format(number + 1))
        else:
            run("ls -t | tail -n +2 | xargs rm -rf")
