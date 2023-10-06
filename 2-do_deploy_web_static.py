#!/usr/bin/python3
"""Compress before sending"""
import os
from fabric.api import env, put, run

env.hosts = ["107.23.95.21", "34.204.81.3"]


def do_deploy(archive_path):
    """
    Write a Fabric script (based on the file 1-pack_web_static.py)
    that distributes an archive to your web servers
    """
    if not os.path.isfile(archive_path):
        return False
    file_path = archive_path.split("/")
    dir_ = "/".join(file_path[:-1])
    file_name = file_path[-1].split(".")[0]
    if put(archive_path, "/tmp/{}.tgz".format(file_name)).failed:
        return False
    if run("mkdir -p /data/web_static/releases/{}/"
            .format(file_name)).failed:
        return False
    if run("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/"
            .format(file_name, file_name)).failed:
        return False
    if run("rm /tmp/{}.tgz".format(file_name)).failed:
        return False
    if run("rm -rf /data/web_static/current").failed:
        return False
    if run("mv /data/web_static/releases/{}/web_static/*\
             /data/web_static/releases/{}/"
            .format(file_name, file_name)).failed:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static"
            .format(file_name)).failed:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(file_name)).failed:
        return False
    return True
