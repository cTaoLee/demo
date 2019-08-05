# -*- coding: utf-8 -*-

from code.db import *

class tester:
    """
    试客模型
    """

    def __init__(self, id):
        self.module = session.query(Tester).filter(Tester.id == id).one()



