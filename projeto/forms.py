# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, RadioField, BooleanField, DateField, SelectField, Label
from wtforms.validators import Required, Length, EqualTo, Email
from werkzeug.datastructures import MultiDict
from flask.ext.wtf import form
from .enums import UsuarioRole


class UsuarioRegistroForm(Form):
	usuario = TextField('Usuário', validators=[Required(' * Campo obrigatório.'), Length(min=5, max=50, message='O nome do usuário deve conter de 5 a 18 caracteres!')])
	matricula = TextField('Matrícula', validators=[Required(' * Campo obrigatório.')])
	email = TextField('E-mail', validators=[Required(' * Campo obrigatório.'), Email('E-mail informado é inválido')])
	role = SelectField('Tipo', choices=[(str(UsuarioRole.admin), "admin"), (str(UsuarioRole.professor), "professor"), (str(UsuarioRole.aluno), "aluno")], default=1)
	senha = PasswordField('Senha', validators=[Required(' *Campo obrigatório.'), Length(min=5, max=20, message='A senha deve conter de 5 a 20 caracteres!')])
	confirma_senha = PasswordField('Confirmação de Senha', validators=[Required(' * Campo obrigatório.'), EqualTo('senha', 'Preencha os campos de senha corretamente!')])


class UsuarioLoginForm(Form):
	matricula = TextField('Matrícula', validators=[Required('Campo obrigatório.')])
	senha = PasswordField('Senha', validators=[Required('Campo obrigatório.')])

