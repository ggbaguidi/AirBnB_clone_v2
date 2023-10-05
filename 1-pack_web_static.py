#!/usr/bin/python3
"""Compress before sending"""
import os
from datetime import datetime
from fabric.api import local

DIR_ = "versions"


def do_pack():
    """
    Fabric script that generates a .tgz
    archive from the contents of the web_static folder
    """
    date = str(datetime.now())\
        .split('.')[0]\
        .replace("-", "")\
        .replace(":", "")\
        .replace(" ", "")

    file_name = "web_static_"+date+".tgz"
    cmd = "tar -cvzf {}/{} web_static".format(DIR_, file_name)

    if not os.path.isdir(DIR_):
        if local("mkdir -p versions").failed:
            return None
    if local(cmd).failed:
        return None
    return file_name
