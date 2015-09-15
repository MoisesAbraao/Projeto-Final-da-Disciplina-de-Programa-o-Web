# -*- coding: utf-8 -*-

import hashlib
import os
from flask import Blueprint, render_template, request, redirect, flash, url_for, send_from_directory
from flask.ext.login import current_user, logout_user, login_user
from sqlalchemy import func, or_
from sqlalchemy.orm import aliased
from .. import app, db, forms
from ..models import *
from ..forms import *
from ..util import login_required
from ..enums import *

from werkzeug import secure_filename


home = Blueprint('home', __name__)

@home.route("/")
@home.route("/login", methods=['GET', 'POST'])
def login():
	form = forms.UsuarioLoginForm()
	#import pdb; pdb.set_trace()
	if form.validate_on_submit():
		usuario = Usuario.query.filter_by(matricula=form.matricula.data, senha=hashlib.md5(form.senha.data.encode('utf-8')).hexdigest(), ativo=True).first()

		if usuario:
			login_user(usuario)
		else:
			flash('Matrícula ou senha inválida!', 'login')

	if not current_user.is_anonymous() and current_user.is_authenticated():
 		return redirect(url_for('home.index'))

	return render_template('home/login.html', form=form)

@home.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home.login'))

@home.route('/index')
@login_required()
def index():

	if current_user.role == UsuarioRole.admin:
		return render_template('home/index_admin.html')
	elif current_user.role == UsuarioRole.professor:
		return render_template('home/index_professor.html')
	elif current_user.role == UsuarioRole.aluno:
		return render_template('home/index_aluno.html')
	else:
		flash(request, 'Erro de autenticação! Entre em contato com um administrador.')
		return redirect(url_for('home.logout'))
		

@home.route("/registro", methods=['GET', 'POST'])
def registro():
	form = UsuarioRegistroForm()
	#import pdb; pdb.set_trace()
	if form.validate_on_submit():
		usuario = (form.usuario.data)
		matricula = (form.matricula.data)
		email = (form.email.data)
		role = (form.role.data)
		senha = (form.senha.data)
		confirma_senha = (form.confirma_senha.data)


		if usuario and matricula and email and senha and (senha == confirma_senha) and role:
			u = Usuario(usuario, matricula, email, senha, role)
			db.session.add(u)
			db.session.commit()


		return redirect(url_for("home.login"))


	if db.session.query(Usuario).count()==0:
		return render_template('home/registro.html', form=form)
	if db.session.query(Usuario).count()>0:
		flash('Você não pode se cadastrar!', 'login')
		return render_template('home/login.html', form=form)
		

@home.route("/registro_de_usuario", methods=['GET', 'POST'])
@login_required()
def registro_de_usuario():
	form = UsuarioRegistroForm()
	#import pdb; pdb.set_trace()
	if form.validate_on_submit():
		usuario = (form.usuario.data)
		matricula = (form.matricula.data)
		email = (form.email.data)
		role = (form.role.data)
		senha = (form.senha.data)
		confirma_senha = (form.confirma_senha.data)


		if usuario and matricula and email and senha and (senha == confirma_senha) and role:
			u = Usuario(usuario, matricula, email, senha, role)
			db.session.add(u)
			db.session.commit()
		flash('Cadastrado com Sucesso!', 'login')
		return redirect(url_for("home.index"))
	
	# if db.session.query(Usuario).count()>1:
	# 	return render_template("home/registro_de_usuario.html", form=form)
	# else:
	return render_template('home/registro_de_usuario.html', form=form)

@home.route("/lista")
def lista():
	usuarios = Usuario.query.all()
	return render_template("home/lista.html", usuarios=usuarios)	

@home.route("/lista_aluno")
def lista_aluno():
	usuarios = Usuario.query.filter(Usuario.role==3)
	return render_template("home/lista_aluno.html", usuarios=usuarios)

@home.route("/lista_professor")
def lista_professor():
	usuarios = Usuario.query.filter(Usuario.role==2)
	return render_template("home/lista_professor.html", usuarios=usuarios)

@home.route("/recupera")
def recupera_senha():
	return render_template('home/recupera_senha.html')

@home.route("/excluir/<int:id>")
def excluir(id):
	usuario = Usuario.query.filter_by(_id=id).first()

	db.session.delete(usuario)
	db.session.commit()
	
	usuarios = Usuario.query.all()
	return redirect(url_for("home.lista", usuarios=usuarios))
	
@home.route("/atualizar/<int:id>", methods=['GET', 'POST'])
@login_required()
def atualizar(id):
	usuario = Usuario.query.filter_by(_id=id).first()
	#import pdb; pdb.set_trace()
	form = UsuarioRegistroForm()

	if form.validate_on_submit():
		usuario = (form.usuario.data)
		matricula = (form.matricula.data)
		email = (form.email.data)
		


		if usuario and matricula and email:
			usuario.usuario = usuario
			usuario.matricula = matricula
			usuario.email = email
			db.session.commit()

		flash('Atualizado com Sucesso!', 'index')
	
	return render_template('home/atualizar.html', usuario=usuario, form=form)


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@home.route("/upload_file", methods=['GET', 'POST'])
@login_required()
def upload_file():

	# import pdb; pdb.set_trace()
	from datetime import datetime

	form = UploadFileForm()

	disciplinas = Disciplina.query.all()
	form.disciplina.choices=[(str(disciplina._id), disciplina.disciplina) for disciplina in disciplinas]

	

	if request.method == "POST":

		descricao = form.descricao.data
		arquivo = request.files['arquivo']


		
	# if form.validate_on_submit():

	# 	arquivo = form.arquivo.data
		
		if arquivo and allowed_file(arquivo.filename):
			filename = secure_filename(arquivo.filename)
			new_filename , new_filename_ext = os.path.splitext(filename)
			new_filename = descricao
			final_filename = str(new_filename+new_filename_ext)

			arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], final_filename))



			flash('Enviado com Sucesso!', 'login')

	# if form.validate_on_submit():
	# 	descricao = form.descricao.data
	# 	arquivo = form.arquivo.data
	# 	disciplina = form.disciplina.data

	# 	if descricao and arquivo and disciplina:
	# 		a = Arquivo(descricao, arquivo, disciplina)
	# 		db.session.add(a)
	# 		db.session.commit()

	return render_template("home/upload_file.html", form=form)

@home.route('/uploads/<final_filename>')
def uploaded_file(final_filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],final_filename)
	

@home.route("/lista_uploads")
def lista_uploads():
	arquivos = Arquivo.query.all()
	return render_template("home/lista_uploads.html", arquivos=arquivos)


@home.route("/registro_de_disciplina", methods=['GET', 'POST'])
@login_required()
def registro_de_disciplina():
	form = DisciplinaRegistroForm()
	#import pdb; pdb.set_trace()

	turmas = Turma.query.all()
	form.turma.choices=[(str(turma._id), turma.turma) for turma in turmas]

	
	if form.validate_on_submit():
		disciplina = (form.disciplina.data)
		turma = (form.turma.data)

		if disciplina and turma:
			d = Disciplina(disciplina, turma)
			db.session.add(d)
			db.session.commit()
		flash('Cadastrado com Sucesso!', 'login')
		return redirect(url_for("home.index"))
	
	return render_template('home/registro_de_disciplina.html', form=form)


@home.route("/lista_disciplina")
def lista_disciplina():
	disciplinas = Disciplina.query.all()
	return render_template("home/lista_disciplina.html", disciplinas=disciplinas)

@home.route("/excluir_disciplina/<int:id>")
def excluir_disciplina(id):
	disciplina = Disciplina.query.filter_by(_id=id).first()

	db.session.delete(disciplina)
	db.session.commit()
	
	disciplinas = Disciplina.query.all()
	return redirect(url_for("home.lista_disciplina", disciplinas=disciplinas))

@home.route("/registro_de_turma", methods=['GET', 'POST'])
@login_required()
def registro_de_turma():
	form = TurmaRegistroForm()

	if form.validate_on_submit():
		turma = (form.turma.data)

		if turma:
			t = Turma(turma)
			db.session.add(t)
			db.session.commit()
		flash('Cadastrado com Sucesso!', 'login')
		return redirect(url_for("home.index"))
	
	return render_template('home/registro_de_turma.html', form=form)

@home.route("/lista_turma")
def lista_turma():
	turmas = Turma.query.all()
	return render_template("home/lista_turma.html", turmas=turmas)


@home.route("/matricula_user", methods=['GET', 'POST'])
@login_required()
def matricula_user():
	form = UsuarioRegistroDisciplinaForm()

	usuarios = Usuario.query.filter(or_(Usuario.role==UsuarioRole.professor, Usuario.role==UsuarioRole.aluno))
	form.usuario.choices=[(str(usuario._id), usuario.usuario) for usuario in usuarios]

	disciplinas = Disciplina.query.all()
	form.disciplina.choices=[(str(disciplina._id), disciplina.disciplina) for disciplina in disciplinas]

	if form.validate_on_submit():
		usuario = (form.usuario.data)
		disciplina = (form.disciplina.data)

		if usuario and disciplina:
			ud = UsuarioDisciplina(usuario, disciplina)
			db.session.add(ud)
			db.session.commit()
		flash('Cadastrado com Sucesso!', 'login')
		return redirect(url_for("home.index"))


	
	return render_template('home/matricula.html', form=form)













