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

import logging
import string

"""
This class cleans cookies we haven't seen before. The basic idea is to
kill sessions, which isn't entirely straight-forward. Since we want this to
be generalized, there's no way for us to know exactly what cookie we're trying
to kill, which also means we don't know what domain or path it has been set for.

The rule with cookies is that specific overrides general. So cookies that are
set for mail.foo.com override cookies with the same name that are set for .foo.com,
just as cookies that are set for foo.com/mail override cookies with the same name
that are set for foo.com/

The best we can do is guess, so we just try to cover our bases by expiring cookies
in a few different ways. The most obvious thing to do is look for individual cookies
and nail the ones we haven't seen coming from the server, but the problem is that cookies are often
set by JavaScript instead of a Set-Cookie header, and if we block those the site
will think cookies are disabled in the browser. So we do the expirations and whitlisting
based on client, server tuples. The first time a client hits a server, we kill whatever
cookies we see then. After that, we just let them through. Not perfect, but pretty effective.
"""
class CookieCleaner:

    """
    Keep track of the DNSCache instance
    """
    _instance = None

    """
    Initialize empty cleaned_cookies object (cleaned_cookies will only be maintained for current runtime)
    """
    def __init__(self):
        self.cleaned_cookies = set();

    """
    Check if the current headers are clean or have been cleaned already during this runtime
    """
    def is_clean(self, method, ip_address_client, host, headers):
        if method == 'POST':
            return True

        if not 'cookie' in headers:
            return True

        return (client, self.get_domain_for_host(host)) in self.cleaned_cookies

    """
    Get the domain for the given host
    """
    def get_domain_for_host(self, host):
        host_parts = host.split('.')
        return '.{0}.{1}'.format(host_parts[-2], host_parts[-1])

    """
    Get the expire headers
    """
    def get_expire_headers(self, method, ip_address_client, host, headers, path):
        domain = self.get_domain_for_host(host)
        self.cleaned_cookies.add((ip_address_client, domain))

        expire_headers = []

        for cookie in headers['cookie'].split(';'):
            cookie = cookie.split('=')[0].strip()
            expire_headers_for_cookie = self.get_expire_string_for_cookie(cookie, host, domain, path)
            expire_headers.extend(expire_headers_for_cookie)
        
        return expire_headers     

    """
    Get the expire string for the given cookie
    """
    def get_expire_string_for_cookie(self, cookie, host, domain, path):
        path_list = path.split('/')
        expire_strings = list()
        
        expire_strings.append("{0}=EXPIRED;Path=/;Domain={1};Expires=Mon, 01-Jan-1990 00:00:00 GMT\r\n".format(cookie, domain))
        expire_strings.append("{0}=EXPIRED;Path=/;Domain={1};Expires=Mon, 01-Jan-1990 00:00:00 GMT\r\n".format(cookie, host))

        if len(path_list) > 2:
            expire_strings.append("{0}=EXPIRED;Path=/{1};Domain={2};Expires=Mon, 01-Jan-1990 00:00:00 GMT\r\n".format(cookie, path_list[1], domain))
            expire_strings.append("{0}=EXPIRED;Path=/{1};Domain={2};Expires=Mon, 01-Jan-1990 00:00:00 GMT\r\n".format(cookie, path_list[1], host))
        
        return expire_strings

    """
    Get the CookieCleaner instance
    """
    def get_instance():
        if CookieCleaner._instance == None:
            CookieCleaner._instance = CookieCleaner()

        return CookieCleaner._instance

    get_instance = staticmethod(get_instance)