# -*- coding: utf-8 -*-
"""
    混合装饰器
"""
import json
import wrapt

from tornado.options import define, options

from sqlalchemy.orm.util import AliasedClass
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.orm.attributes import InstrumentedAttribute

from ..db import session

# 默认配置
define('ROWS_COUNT', default='totle', type=str)
define('ROWS_DATA', default='data', type=str)


def analyze_table(table: any) -> tuple:
    """
    解析表
    :param table:
    :return:
    """
    if isinstance(table, list):
        return table[0], table[1:]
    elif isinstance(table, AliasedClass) or isinstance(table, DeclarativeMeta):
        return table, None
    else:
        raise Exception('param table is invalid!')


def analyze_function(result: any) -> dict:
    """
    解析函数结果
    :param result:
    :return:
    """
    res = {}
    if isinstance(result, dict):
        res['where'] = result
    elif isinstance(result, list):
        res['field'] = result
    elif callable(result):
        res['callback'] = result
    elif isinstance(result, tuple):
        for i in result:
            res.update(analyze_function(i))
    elif result is None:
        pass
    else:
        raise Exception('func result is unresolved!')
    return res


def as_dict(fields, item):
    """
    查询结果转字典
    :param fields:
    :param item:
    :return:
    """
    if hasattr(item, '__table__'):
        return {c.name: getattr(item, c.name, None) for c in item.__table__.columns}
    else:
        fields = [field.key for field in fields]
        return dict(zip(fields, item))


def select(table, type_='rows'):
    """
    查询混合
    :param type_:
    :param table: 表名
    :return:
    """
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        func_result = analyze_function(wrapped(*args, **kwargs))
        main_table, join_table = analyze_table(table)

        if func_result.get('field', None):
            query = session.query(*func_result.get('field'))
        else:
            query = session.query(main_table)

        # 处理连表
        if join_table:
            for t in join_table:
                query = query.outerjoin(*t)

        # 处理查询条件
        if func_result.get('where', None):
            for key, value in func_result.get('where').items():
                if isinstance(key, InstrumentedAttribute):
                    query = query.filter(key == value)
                elif callable(key):
                    if isinstance(value, dict):
                        value = [k == v for k, v in value.items()]
                    query = query.filter(key(*value))

        # 处理回调函数
        if func_result.get('callback', None):
            callback = func_result.get('callback')
        else:
            def callback(data): return data

        if type_ == 'rows':
            count = query.count()
            items = query.all()
            data = [callback(as_dict(func_result.get('field', None), item)) for item in items]
            result = {
                options.ROWS_COUNT: count,
                options.ROWS_DATA: data
            }
        else:
            result = query.all()

        # 数据输出
        instance.write(json.dumps(result))

    return wrapper