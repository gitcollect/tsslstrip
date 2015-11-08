#!/usr/bin/env python

import config
import sys
import getopt
import logging
import traceback
import string
import os

#from twisted.web import http
#from twisted.internet import reactor

#from sslstrip.StrippingProxy import StrippingProxy
#from sslstrip.URLMonitor import URLMonitor
#from sslstrip.CookieCleaner import CookieCleaner

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
                port = arg

        return (log_file, port)

    except getopt.GetoptError:           
        usage()                          
        sys.exit(2)                         

def main(argv):
    (log_file, port) = parse_options(argv)
        
    logging.basicConfig(
        level=logging.WARNING, 
        format='%(asctime)s %(message)s',
        filename=log_file, 
        filemode='w'
    )

    #strippingFactory              = http.HTTPFactory(timeout=10)
    #strippingFactory.protocol     = StrippingProxy

    #reactor.listenTCP(int(port), strippingFactory)

    print('Targeted SSLSTRIP v{0}'.format(config.version))
    print('Running...')
    print('')

    #reactor.run()

if __name__ == '__main__':
    main(sys.argv[1:])
