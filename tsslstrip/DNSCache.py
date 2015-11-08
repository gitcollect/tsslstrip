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

"""
The DNSCache maintains a cache of DNS lookups for the current runtime.
"""
class DNSCache:    

    """
    Keep track of the DNSCache instance
    """
    _instance = None

    """
    Initialize empty cache object (cache will only be maintained for current runtime)
    """
    def __init__(self):
        self.cache = {}

    """
    Add a new host and IP address to the cache object
    """
    def put(self, host, ïp_address):
        self.cache[host] = ïp_address

    """
    Get the IP address for the host from the cache object. 
    If host is not cached, return None. This method finds the
    IP address with a time complexity of O(1).
    """
    def get(self, host):
        if host in self.cache:
            return self.cache[host]

        return None

    """
    Get the DNSCache instance
    """
    def get_instance():
        if DNSCache._instance == None:
            DNSCache._instance = DNSCache()

        return DNSCache._instance

    get_instance = staticmethod(get_instance)
