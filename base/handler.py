# -*- coding: utf-8 -*-
import json
import os
import re
import traceback
from typing import Any

import inspect

import tornado.web
from tornado import httputil
from tornado.web import Application
from tornado.options import define, options


# 默认配置
define('login_url', default='/login.html', type=str)
define('error_format', default='json', type=str)


class BindHandler(tornado.web.RequestHandler):
    """
    绑定控制器，使控制器支持绑定模式
    """
    def get(self):
        self.execute_bind_handler('GET')

    def post(self):
        self.execute_bind_handler('POST')

    def put(self):
        self.execute_bind_handler('PUT')

    def patch(self):
        self.execute_bind_handler('PATCH')

    def delete(self):
        self.execute_bind_handler('DELETE')

    def execute_bind_handler(self, http_method):
        if options.route_type != 'bind':
            raise tornado.web.HTTPError(404)

        for o in dir(self):
            attr = getattr(self, o)
            # 寻找拥有 _path 属性且和请求地址相符合的方法
            if hasattr(attr, '_path') and inspect.ismethod(attr) and self.at_path(attr._path):
                if http_method != self.request.method:
                    raise tornado.web.HTTPError(500, 'Method %s is not all allow!' % self.request.method)

                method = attr
                params = [x for x in self.request.path.split('/') if x not in attr._path.split('/')]
                kwargs = dict(zip(attr._params, params))
                method(**kwargs)

    def at_path(self, path):
        """
        判断当前访问路径是否符合规则
        :param path:
        :return:
        """
        if not path.endswith('$'):
            path += '/?$'
        r = re.compile(path)
        return r.match(self.request.path)

    @classmethod
    def get_paths(cls):
        """
        获取该类所有绑定路由的路由地址
        :return:
        """
        paths = []
        for f in dir(cls):
            o = getattr(cls, f)
            if callable(o) and hasattr(o, '_path'):
                paths.append(getattr(o, '_path'))
        return paths


def bind_route(method, _path):
    """
    装饰绑定控制器，将路由信息装饰在方法内（这是为了实现路由的绑定模式）
    :param method:
    :param _path:
    :return:
    """
    def wrapper(func):
        def handler_method(*args, **kwargs):
            return func(*args, **kwargs)
        handler_method._path = re.sub(r'(?<={)\w+}', '.*', _path).replace('{', '')
        handler_method._params = re.findall(r'(?<={)\w+', _path)
        handler_method._method = method
        return handler_method
    return wrapper


def get(_path):
    return bind_route('get', _path)


def post(_path):
    return bind_route('post', _path)


def put(_path):
    return bind_route('put', _path)


def patch(_path):
    return bind_route('patch', _path)


def delete(_path):
    return bind_route('delete', _path)


class WebHandler(BindHandler):

    def __init__(self, application: "Application", request: httputil.HTTPServerRequest, **kwargs: Any):
        super().__init__(application, request, **kwargs)

        file = inspect.getfile(self.__class__)
        config_file = os.path.dirname(file) + '/config'
        tornado.options.parse_config_file(config_file)

    def get_login_url(self):
        """
        配置当前登录页
        :return:
        """
        return options.login_url

    def write_error(self, status_code: int, **kwargs: Any):
        """
        处理错误输出
        :param status_code:
        :param kwargs:
        :return:
        """
        if options.error_format == 'json':
            res = {
                'base': str(status_code),
                'msg': str(kwargs['exc_info'][1])
            }
            if options.debug:
                res['traceback'] = traceback.format_exception(*kwargs["exc_info"])
            self.write(json.dumps(res))
        else:
            super().write_error(status_code, **kwargs)

    def get_current_user(self):

        pass


