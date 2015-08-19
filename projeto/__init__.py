# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager


# cria a aplicacao e informa qual arquivo contem os parametros de configuracao
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')


# cria o objeto de banco de dados da aplicacao
db = SQLAlchemy(app)


from .models import Usuario


lm = LoginManager()
lm.init_app(app)
lm.login_view = 'home.login'


@lm.user_loader
def load_user(id):
    return db.session.query(Usuario).filter_by(_id=id).first()


# registra os Blueprint's
from .views.home import home


app.register_blueprint(home)