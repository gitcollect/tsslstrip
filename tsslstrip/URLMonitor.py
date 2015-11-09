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

import re

"""
The URL monitor maintains a set of (client, url) tuples that correspond to requests which the
server is expecting over SSL.
"""
class URLMonitor:    

    """
    Keep track of the URLMonitor instance
    """
    _instance = None

    """
    Initialize empty stripped urls and ports object (these will only be maintained for current runtime)
    """
    def __init__(self):
        self.stripped_urls = set()
        self.stripped_url_ports = {}

    def is_secure_link(self, client, url):
        return (client, url) in self.stripped_urls

    def get_secure_port(self, client, url):
        if (client, url) in self.stripped_urls:
            return self.stripped_url_ports[(client, url)]
        else:
            return 443

    def add_secure_link(self, client, url):
        method_index = url.find("//") + 2
        method = url[0:method_index]

        path_index = url.find("/", method_index)
        host = url[method_index:path_index]
        path = url[path_index:]

        port = 443
        port_index = host.find(":")

        if (port_index != -1):
            host = host[0:port_index]
            port = host[port_index+1:]
            if len(port) == 0:
                port = 443
        
        url = method + host + path

        self.stripped_urls.add((client, url))
        self.stripped_url_ports[(client, url)] = int(port)

    """
    Get the URLMonitor instance
    """
    def get_instance():
        if URLMonitor._instance == None:
            URLMonitor._instance = URLMonitor()

        return URLMonitor._instance

    get_instance = staticmethod(get_instance)
