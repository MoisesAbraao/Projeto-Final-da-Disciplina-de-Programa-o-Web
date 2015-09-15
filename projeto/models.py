# -*- coding: utf-8 -*-
from sqlalchemy import ForeignKey, and_, or_, text
from sqlalchemy.orm import relationship, aliased
from sqlalchemy.sql.expression import func
from . import db
from enums import UsuarioRole
import hashlib
from datetime import datetime


class Usuario(db.Model):
	__tablename__ = 'usuario'

	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	usuario = db.Column(db.String(50), unique=True)
	matricula = db.Column(db.String, unique=True)
	email = db.Column(db.String, unique=True)
	senha = db.Column(db.String(32))
	role = db.Column(db.Integer)
	ativo = db.Column(db.Boolean)



	def __init__(self, usuario, matricula, email, senha, role=UsuarioRole.aluno):
		self.usuario = usuario
		self.matricula = matricula
		self.email = email.lower()
		self.senha = hashlib.md5(senha.encode('utf-8')).hexdigest()
		self.role = role
		self.ativo = True



	def is_authenticated(self):
		return True

	def is_active(self):
		return self.ativo

	def is_anonymous(self):
		return False

	def is_admin(self):
		return self.role == UsuarioRole.admin

	def get_id(self):
		return self._id

	def get_role(self):
		return self.role





class Turma(db.Model):
	__tablename__ = 'turma'

	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	turma = db.Column(db.String(12), unique=True)
	

	def __init__(self, turma):
		self.turma = turma




class Disciplina(db.Model):
	__tablename__ = 'disciplina'

	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	disciplina = db.Column(db.String(50), unique=True)
	turma_id = db.Column(db.Integer, ForeignKey("turma._id"))

	def __init__(self, disciplina, turma_id):
		self.disciplina = disciplina
		self.turma_id = turma_id



class UsuarioDisciplina(db.Model):
	__tablename__ = 'usuario_disciplina'

	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	usuario_id = db.Column(db.Integer, ForeignKey("usuario._id"))
	disciplina_id = db.Column(db.Integer, ForeignKey("disciplina._id"))

	def __init__(self, usuario_id, disciplina_id):
		self.usuario_id = usuario_id
		self.disciplina_id = disciplina_id




class Arquivo(db.Model):
	__tablename__ = "uploads"

	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	descricao = db.Column(db.String(50))
	arquivo = db.Column(db.String)
	disciplina_id = db.Column(db.Integer, ForeignKey("disciplina._id"))

	def __init__(self, descricao, arquivo, disciplina_id):
		self.descricao = descricao
		self.arquivo = arquivo
		self.disciplina_id = disciplina_id



