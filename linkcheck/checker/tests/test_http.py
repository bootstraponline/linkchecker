# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2006 Bastian Kleineidam
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
Test http checking.
"""

import unittest
import os
import re

import linkcheck.checker.tests.httptest


class TestHttp (linkcheck.checker.tests.httptest.HttpServerTest):
    """
    Test http:// link checking.
    """

    def test_html (self):
        try:
            self.start_server(handler=CookieRedirectHttpRequestHandler)
            url = u"http://localhost:%d/linkcheck/checker/tests/data/" \
                  u"http.html" % self.port
            resultlines = self.get_resultlines("http.html")
            self.direct(url, resultlines, recursionlevel=1, cmdline=True)
            self.redirect_http_test()
            self.noproxyfor_test()
        finally:
            self.stop_server()

    def test_redirect (self):
        try:
            self.start_server(handler=RedirectHttpsRequestHandler)
            self.redirect_https_test()
        finally:
            self.stop_server()

    def redirect_https_test (self):
        url = u"http://localhost:%d/redirect1" % self.port
        nurl = url
        rurl = url.replace('redirect', 'newurl')
        resultlines = [
            u"url %s" % url,
            u"cache key %s" % nurl,
            u"real url %s" % nurl,
            u"info Redirected to %s." % rurl.replace('http:', 'https:'),
            u"info The redirected URL is outside of the domain filter, " \
            u"checked only syntax.",
            u"warning Redirection to different URL type encountered; the " \
            u"original URL was u'http://localhost:%d/redirect1'." % self.port,
            u"valid",
        ]
        self.direct(url, resultlines, recursionlevel=0, cmdline=True)

    def redirect_http_test (self):
        url = u"http://localhost:%d/redirect1" % self.port
        nurl = url
        rurl = url.replace("redirect", "newurl")
        resultlines = [
            u"url %s" % url,
            u"cache key %s" % nurl,
            u"real url %s" % rurl,
            u"info Redirected to %s." % rurl,
            u"error",
        ]
        self.direct(url, resultlines, recursionlevel=0, cmdline=True)
        url = u"http://localhost:%d/linkcheck/checker/tests/data/redirect.html" % \
              self.port
        nurl = url
        rurl = url.replace("redirect", "newurl")
        resultlines = [
            u"url %s" % url,
            u"cache key %s" % nurl,
            u"real url %s" % rurl,
            u"info Redirected to %s." % rurl,
            u"valid",
            u"url newurl.html (cached)",
            u"cache key %s" % nurl.replace("redirect", "newurl"),
            u"real url %s" % rurl.replace("redirect", "newurl"),
            u"name Recursive Redirect",
            u"valid",
        ]
        self.direct(url, resultlines, recursionlevel=99, cmdline=True)

    def noproxyfor_test (self):
        """
        Test setting proxy and --no-proxy-for option.
        """
        os.environ["http_proxy"] = "http://imadoofus:8877"
        confargs = {"noproxyfor": [re.compile("localhost")]}
        url = u"http://localhost:%d/linkcheck/checker/tests/data/http.html" % \
              self.port
        nurl = url
        resultlines = [
            u"url %s" % url,
            u"cache key %s" % nurl,
            u"real url %s" % nurl,
            u"info Ignoring proxy setting 'imadoofus:8877'",
            u"valid",
        ]
        self.direct(url, resultlines, recursionlevel=0,
                    confargs=confargs, cmdline=True)
        del os.environ["http_proxy"]


def get_cookie (maxage=2000):
    data = (
        ("Comment", "justatest"),
        ("Max-Age", "%d" % maxage),
        ("Path", "/"),
        ("Version", "1"),
        ("Foo", "Bar"),
    )
    parts = ['%s="%s"' % (key, value) for key, value in data]
    return "; ".join(parts)


class CookieRedirectHttpRequestHandler (linkcheck.checker.tests.httptest.NoQueryHttpRequestHandler):
    """
    Handler redirecting certain requests, and setting cookies.
    """

    def end_headers (self):
        """
        Send cookie before ending headers.
        """
        self.send_header("Set-Cookie", get_cookie())
        self.send_header("Set-Cookie", get_cookie(maxage=0))
        super(CookieRedirectHttpRequestHandler, self).end_headers()

    def redirect (self):
        """
        Redirect request.
        """
        path = self.path.replace("redirect", "newurl")
        self.send_response(302)
        self.send_header("Location", path)
        self.end_headers()

    def do_GET (self):
        """
        Removes query part of GET request.
        """
        if "redirect" in self.path:
            self.redirect()
        else:
            super(CookieRedirectHttpRequestHandler, self).do_GET()

    def do_HEAD (self):
        if "redirect" in self.path:
            self.redirect()
        else:
            super(CookieRedirectHttpRequestHandler, self).do_HEAD()

class RedirectHttpsRequestHandler (CookieRedirectHttpRequestHandler):

    def redirect (self):
        """
        Redirect request.
        """
        path = self.path.replace("redirect", "newurl")
        port = self.server.server_address[1]
        url = "https://localhost:%d%s" % (port, path)
        self.send_response(302)
        self.send_header("Location", url)
        self.end_headers()

def test_suite ():
    """
    Build and return a TestSuite.
    """
    return unittest.makeSuite(TestHttp)


if __name__ == '__main__':
    unittest.main()