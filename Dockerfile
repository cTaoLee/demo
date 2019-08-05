FROM python

RUN pip install tornado
RUN pip install cymysql sqlalchemy
RUN pip install pika

RUN pip install baidu-aip

RUN pip install wrapt