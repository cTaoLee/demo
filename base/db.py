# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy import and_, or_, between
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, aliased

engine = create_engine("mysql+cymysql://root:root@mysql:3306/brush_order")
connection = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()

Base = automap_base()
Base.prepare(engine, reflect=True)

"""
表模型
"""
Tester = getattr(Base.classes, 'tester')
Salesman = getattr(Base.classes, 'salesman')
User = getattr(Base.classes, 'user')