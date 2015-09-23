# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, FileField, PasswordField, TextAreaField, RadioField, BooleanField, DateField, SelectField, Label
from wtforms.validators import Required, Length, EqualTo, Email
from werkzeug.datastructures import MultiDict
from flask.ext.wtf import form
from .enums import UsuarioRole


class UsuarioRegistroForm(Form):
	usuario = TextField('Usuário', validators=[Required(' * Campo obrigatório.'), Length(min=5, max=50, message='O nome do usuário deve conter de 5 a 50 caracteres!')])
	matricula = TextField('Matrícula', validators=[Required(' * Campo obrigatório.')])
	email = TextField('E-mail', validators=[Required(' * Campo obrigatório.'), Email('E-mail informado é inválido')])
	role = SelectField('Tipo', choices=[(str(UsuarioRole.admin), "admin"), (str(UsuarioRole.professor), "professor"), (str(UsuarioRole.aluno), "aluno")], default=1)
	senha = PasswordField('Senha', validators=[Required(' *Campo obrigatório.'), Length(min=5, max=20, message='A senha deve conter de 5 a 20 caracteres!')])
	confirma_senha = PasswordField('Confirmação de Senha', validators=[Required(' * Campo obrigatório.'), EqualTo('senha', 'Preencha os campos de senha corretamente!')])
	



class UsuarioLoginForm(Form):
	matricula = TextField('Matrícula', validators=[Required('Campo obrigatório.')])
	senha = PasswordField('Senha', validators=[Required('Campo obrigatório.')])



class UploadFileForm(Form):
	descricao = TextField('Descrição', validators=[Required(' * Campo obrigatório.'), Length(min=5, max=50, message='A Descrição deve conter de 5 a 50 caracteres!')])
	arquivo = FileField('Arquivo', validators=[Required('Campo obrigatório.')])
	disciplina = SelectField('Disciplina', validators=[Required('Selecione uma Disciplina!')])



class DisciplinaRegistroForm(Form):
	disciplina = TextField('Disciplina', validators=[Required(' * Campo obrigatório.'), Length(min=5, max=50, message='O nome do disciplina deve conter de 5 a 50 caracteres!')])
	turma = SelectField('Turma', validators=[Required('Selecione uma Turma!')])



class TurmaRegistroForm(Form):
	turma = TextField('Turma', validators=[Required(' * Campo obrigatório.'), Length(min=5, max=50, message='O nome da Turma deve conter de 5 a 50 caracteres!')])

class UsuarioRegistroDisciplinaForm(Form):
	usuario = SelectField('Usuário', validators=[Required('Selecione um Usuário!')])
	disciplina = SelectField('Disciplina', validators=[Required('Selecione uma Disciplina!')])

class EditaUsuarioForm(Form):
	usuario = Label('usuario', '')
	matricula = Label('matricula', '')
	email = Label('email', '')

	def init_from_Usuario(self, usuario):
		self.usuario = usuario.usuario
		self.matricula = usuario.matricula
		self.email = usuario.email



