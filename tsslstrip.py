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
import getopt
import logging

from twisted.web import http
from twisted.internet import reactor

from tsslstrip.StrippingProxy import StrippingProxy
from tsslstrip.URLMonitor import URLMonitor
from tsslstrip.CookieCleaner import CookieCleaner

def usage():
    print('Targeted SSLSTRIP v{0}'.format(config.version))
    print('Usage: tsslstrip <options>')
    print('')
    print('Options:')
    print('-w <filename>,   --write=<filename>    Specify file to log to (optional).')
    print('-l <port>,       --listen=<port>       Port to listen on (default 10000).')
    print('-h,              --help                Print this help message.')
    print('')

"""
Get CLI arguments
"""
def parse_options(argv):
    log_file = 'tsslstrip.log'
    port = 10000
    
    try:                                
        opts, args = getopt.getopt(argv, 'hw:l:psafk', ['help', 'write=', 'listen='])

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                usage()
                sys.exit()
            elif opt in ('-w', '--write'):
                logFile = arg
            elif opt in ('-l', '--listen'):
                port = int(arg)

        return (log_file, port)

    except getopt.GetoptError:           
        usage()                          
        sys.exit(2)                         

def main(argv):
    (log_file, port) = parse_options(argv)
        
    logging.basicConfig(
        level=logging.DEBUG, 
        format='%(asctime)s %(message)s',
        filename=log_file, 
        filemode='w'
    )

    stripping_factory = http.HTTPFactory(timeout = 10)
    stripping_factory.protocol = StrippingProxy
    reactor.listenTCP(port, stripping_factory)

    print('Targeted SSLSTRIP v{0}'.format(config.version))
    print('Running...')
    print('')

    reactor.run()

if __name__ == '__main__':
    main(sys.argv[1:])
