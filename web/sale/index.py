# -*- coding: utf-8 -*-

import tornado.web

from code.handler import WebHandler


class MainHandler(WebHandler):
    """

    """
    @tornado.web.authenticated
    def get(self):
        return self.redirect('/static/admin/login.html')