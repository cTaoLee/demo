# -*- coding: utf-8 -*-

import tornado.web

from base.handler import WebHandler, get


class MainHandler(WebHandler):
    """

    """
    @tornado.web.authenticated
    def get(self):
        return self.redirect('/static/admin/index.html')



class TestHandler(WebHandler):
    @get('/xx')
    def h(self):
        return 1

    @get('/xxx/{xx}')
    def hx(self, xx):
        self.write(xx)