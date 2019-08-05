# -*- coding: utf-8 -*-
import inspect
import os
import re
import sys

from tornado.options import define, options
from tornado.util import import_object

from .handler import WebHandler

# 默认配置
define('route_type', default='bind', type=str)
define('route_list', default=[], type=list)
define('handler', default='handler', type=str)
define('handler_name', default='MainHandler', type=str)
define('default_handler', default='index', type=str)





def get_handler_file():
    """
    获取 handler 目录下的所有 .py 文件
    :return:
    """
    if not os.path.exists(options.handler):
        raise Exception('目录不存在')
    return [
        os.path.join(root, file)
        for root, dirs, files in os.walk(options.handler)
        for file in files if file.endswith('.py')
    ]


def get_route():
    """
    :return:
    """
    route = []

    # 通过文件找到控制器
    if options.route_type == 'dir':
        for file in get_handler_file():
            _class_name = file[:-3].replace('/', '.') + '.%s' % options.handler_name
            _path_name = file[:-3].replace(options.handler, '')
            try:
                route.append((_path_name, import_object(_class_name)))
                # 假如默认控制器则可以省略
                _path_list = _path_name.split('/')
                if _path_list[-1] == options.default_handler:
                    length = len(options.default_handler) + 1
                    route.append((_path_name[:-length], import_object(_class_name)))
            except Exception:
                pass

    # 通过类名找到控制器
    elif options.route_type == 'class':
        p = re.compile(r'([a-z]|\d)([A-Z])')

        for file in get_handler_file():
            _class_name = file[:-3].replace('/', '.')
            _path_name = file[:-3].replace(options.handler, '')
            try:
                __import__(_class_name)
                for name, _class in inspect.getmembers(sys.modules[_class_name]):
                    if inspect.isclass(_class) and issubclass(_class, WebHandler) and _class is not WebHandler:
                        name = re.sub(p, r'\1_\2', name).lower()
                        if name.endswith('_handler'):
                            route.append((os.path.join(_path_name, name[:-8]), _class))
            except Exception:
                pass

    # 通过后置绑定获取控制器
    elif options.route_type == 'bind':
        for file in get_handler_file():
            _class_name = file[:-3].replace('/', '.')
            try:
                __import__(_class_name)
                for name, _class in inspect.getmembers(sys.modules[_class_name]):
                    if inspect.isclass(_class) and issubclass(_class, WebHandler) and _class is not WebHandler:
                        for _path in _class.get_paths():
                            path = re.sub(r'(?<={)\w+}', '.*', _path).replace('{', '')
                            route.append((path + '/?', _class))
            except Exception as e:
                pass
    print(route)
    return route



