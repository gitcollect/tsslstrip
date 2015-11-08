#!/usr/bin/env python

import config
import sys
import os
import shutil

from distutils.core import setup
from distutils.core import Extension

class Installation:

    """
    TSSLSTRIP installation
    """
    def __init__(self):
        print('Installing {0} ...'.format(config.name))
        shutil.copyfile('tsslstrip.py', 'tsslstrip/tsslstrip')
        setup(
            name = 'tsslstrip',
            version = config.version,
            description = config.description,
            author = config.author,
            author_email = config.author_email,
            license = 'GPL',
            packages = ['tsslstrip'],
            packages_dir = {'tsslstrip' : 'tsslstrip/'},
            scripts = ['tsslstrip/tsslstrip'],
            data_files = [('share/tsslstrip', ['README', 'LICENSE'])]
        )

        print('Cleaning up build directory...')
        self.remove_all('build/')
        self.remove_generic('tsslstrip/tsslstrip', os.remove)

        print('Installation complete.')
        print('Happy stripping!')

    """
    Delete the given folder and contents
    """
    def remove_all(self, path):
        if not os.path.isdir(path):
            return

        files = os.listdir(path)

        for afile in files:
            fullpath = os.path.join(path, afile)
            if os.path.isfile(fullpath):
                self.remove_generic(fullpath, os.remove)
            elif os.path.isdir(fullpath):
                self.removeall(fullpath)
                self.remove_generic(fullpath, os.rmdir)

        self.remove_generic(path, os.rmdir)

    """
    Run given function with path as parameter. Catches OSError
    """
    def remove_generic(path, __func__):
        try:
            __func__(path)
        except OSError, (errno, strerror, filename):
            print('File could not be deleted: {0}'.format(filename))
            print('Got exception: {0}'.format(strerror))

Installation()
