import pika
from inspect import isfunction

import tornado
from tornado.options import options, define


# 默认配置
define('amqp_url', default='amqp://guest:guest@rabbitmq/%2f', type=str)
define('queue', default={}, type=dict)

tornado.options.parse_config_file("config")
parameter = pika.connection.URLParameters(url=options.amqp_url)
connection = pika.BlockingConnection(parameters=parameter)
channel = connection.channel()
channel.basic_qos(prefetch_count=1)

# 绑定队列
for name in options.queue:
    info = options.queue[name]
    if isinstance(info, dict):
        pass
    elif isfunction(info):
        channel.queue_declare(queue=name)
        channel.basic_consume(name, info)
    elif isfunction(info.run):
        channel.queue_declare(queue=name)
        channel.basic_consume(name, info.run)
    else:
        raise Exception('不支持的类型')

channel.start_consuming()