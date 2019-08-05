# -*- coding: utf-8 -*-
from code.db import *

def sign_in(type_, username, password=None, captcha=None):
    if type_ == 'admin_default':
        q = session.query().filter(User.username == username, User.password == password)
        print(session.query(q.exists()).scalar())
        if session.query(q.exists()).scalar():
            return True
    return False

def sign_in_by_module(module):
    pass