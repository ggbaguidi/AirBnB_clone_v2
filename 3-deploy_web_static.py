#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
import os.path
from datetime import datetime
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run

env.hosts = ["107.23.95.21", "34.204.81.3"]


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


def do_deploy(archive_path):
    """
    Write a Fabric script (based on the file 1-pack_web_static.py)
    that distributes an archive to your web servers
    """
    if not os.path.isfile(archive_path):
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True


def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if not file:
        return False
    return do_deploy(file)
