#!/usr/bin/env python

# Copyright (c) 2004-2015 Moxie Marlinspike, Tijme Gommers
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

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
