# -*- coding: utf-8 -*-
from abc import ABC

from base.handler import WebHandler
from module.sign import sign_in


class MainHandler(WebHandler, ABC):
    """
    注册登录相关
    """
    def post(self):
        """
        普通登录
        :return:
        """
        username = self.get_argument('username')
        password = self.get_argument('password')

        if sign_in('admin_default', username=username, password=password):
            print(1)
        else:
            print(0)

