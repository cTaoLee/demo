# -*- coding: utf-8 -*-
import os

import tornado.web
import tornado.ioloop
from tornado.options import define, options

from .route import get_route

# 默认配置
define('port', default=80, type=int)
define('debug', default=True, type=bool)
define('static_path', default='./static', type=str)


def run_app():
    """
    启动 app 函数
    :return:
    """

    # 加载配置文件
    tornado.options.parse_command_line()
    tornado.options.parse_config_file("config")

    # 生成路由列表
    route = get_route()

    application = tornado.web.Application(
        route,
        debug=options.debug,
        static_path=os.path.realpath(options.static_path)
    )
    application.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
