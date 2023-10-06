#!/usr/bin/python3
"""Compress before sending"""
import os
from datetime import datetime
from fabric.api import env, put, run, local

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
    - Upload the archive to the /tmp/ directory of the web server
    - iUncompress the archive to the folder /data/web_static/releases/<archive
    filename without extension> on the web server
    - Delete the archive from the web server
    - Delete the symbolic link /data/web_static/current from the web server
    - Create a new the symbolic link /data/web_static/current on the web
    server, linked to the new version of your code
    (/data/web_static/releases/<archive filename without extension>)
    """
    if not (os.path.exists(archive_path)):
        return False
    archive_name = archive_path.split('/')[1]
    archive_name_without_ext = archive_path.split('/')[1].split('.')[0]
    release_path = '/data/web_static/releases/' + archive_name_without_ext
    upload_path = '/tmp/' + archive_name
    put(archive_path, upload_path)
    run('mkdir -p ' + release_path)
    run('tar -xzf ' + upload_path + ' -C ' + release_path)
    run('rm ' + upload_path)
    run('mv ' + release_path + '/web_static/* ' + release_path + '/')
    run('rm -rf ' + release_path + '/web_static')
    run('rm -rf /data/web_static/current')
    run('ln -s ' + release_path + ' /data/web_static/current')
    return True
