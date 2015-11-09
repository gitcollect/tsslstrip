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

import urlparse
import logging
import os
import sys
import random

from twisted.web.http import Request
from twisted.web.http import HTTPChannel
from twisted.web.http import HTTPClient

from twisted.internet import ssl
from twisted.internet import defer
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory

from ServerConnectionFactory import ServerConnectionFactory
from ServerConnection import ServerConnection
from SSLServerConnection import SSLServerConnection
from URLMonitor import URLMonitor
from CookieCleaner import CookieCleaner
from DNSCache import DNSCache

"""
This class represents incoming client requests and is essentially where
the magic begins. Here we remove the client headers we dont like, and then
respond with either session denial, or proxy through HTTP
or SSL to the server.
"""
class ClientRequest(Request):

    """
    Construct ClientRequest using Twisted Internet Reactor
    """
    def __init__(self, channel, queued, reactor = reactor):
        Request.__init__(self, channel, queued)
        self.reactor = reactor
        self.url_monitor = URLMonitor.get_instance()
        self.cookie_cleaner = CookieCleaner.get_instance()
        self.dns_cache = DNSCache.get_instance()

    """
    Process the client request (called by Twisted Web)
    """
    def process(self):
        host = self.getHeader('host')

        logging.debug('Resolving host: {0}'.format(host)
        deferred = self.resolve_host(host)

        deferred.addCallback(self.host_resolved_success)
        deferred.addErrback(self.host_resolved_error)

    """
    Check if host is cached in DNS Cache, otherwise resolve it
    """
    def resolve_host(self, host):
        ip_address = self.dns_cache.get(host)

        if ip_address != None:
            logging.debug('Host was cached')
            return defer.succeed(ip_address)
        else:
            logging.debug('Host not cached')
            return reactor.resolve(host)

    """
    When host got resolved to an IP address successfully
    """
    def host_resolved_success(self, ip_address):
        host = self.getHeader('host')

        logging.debug('Resolved host successfully: {0} -> {1}'.format(host, ip_address))

        headers = self.cleanHeaders()
        ip_address_client = self.getClientIP()
        path = self.getPathFromUri()

        self.content.seek(0, 0)
        post_data = self.content.read()
        url = 'http://' + host + path

        self.dns_cache.put(host, address)

        if (not self.cookieCleaner.is_clean(self.method, ip_address_client, host, headers)):
            logging.debug('Sending expired cookies...')
            self.send_expired_cookies(host, path, self.cookie_cleaner.get_expire_headers(self.method, ip_address_client, host, headers, path))
        elif (self.url_monitor.isSecureLink(ip_address_client, url)):
            logging.debug('Sending request via SSL...')
            self.proxyViaSSL(address, self.method, path, postData, headers, self.url_monitor.get_secure_port(ip_address_client, url))
        else:
            logging.debug('Sending request via HTTP...')
            self.proxyViaHTTP(address, self.method, path, postData, headers)

    """
    Send the expired cookie headers and finish the request
    """
    def send_expired_cookies(self, host, path, expire_headers):
        self.setResponseCode(302, 'Moved')
        self.setHeader('Connection', 'close')
        self.setHeader('Location', 'http://' + host + path)
        
        for header in expire_headers:
            self.setHeader('Set-Cookie', header)

        self.finish()  





    def host_resolved_error(self, error):
        logging.warning("Host resolution error: " + str(error))
        self.finish()
        
    def proxyViaHTTP(self, host, method, path, postData, headers):
        connectionFactory          = ServerConnectionFactory(method, path, postData, headers, self)
        connectionFactory.protocol = ServerConnection
        self.reactor.connectTCP(host, 80, connectionFactory)

    def proxyViaSSL(self, host, method, path, postData, headers, port):
        clientContextFactory       = ssl.ClientContextFactory()
        connectionFactory          = ServerConnectionFactory(method, path, postData, headers, self)
        connectionFactory.protocol = SSLServerConnection
        self.reactor.connectSSL(host, port, connectionFactory, clientContextFactory)
      

    def cleanHeaders(self):
        headers = self.getAllHeaders().copy()

        if 'accept-encoding' in headers:
            del headers['accept-encoding']

        if 'if-modified-since' in headers:
            del headers['if-modified-since']

        if 'cache-control' in headers:
            del headers['cache-control']

        return headers

    def getPathFromUri(self):
        if (self.uri.find("http://") == 0):
            index = self.uri.find('/', 7)
            return self.uri[index:]

        return self.uri