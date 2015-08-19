# -*- coding: utf-8 -*-
import os
# db generico
SQLALCHEMY_DATABASE_URI = 'sqlite:///' +  os.path.join(os.path.abspath('.'), 'db.sqlite')
SECRET_KEY = os.urandom(32)
# forms
CSRF_ENABLED = True


DEBUG = True