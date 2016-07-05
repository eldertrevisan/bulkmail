# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#
#Copyright 2016 Elder Sanitá Trevisan
#
#This file is part of BulkMail.
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#------------------------------------------------------------------------------

import locale
try:
	locale.setlocale(locale.LC_ALL, 'pt_BR')
except:
	locale.setlocale(locale.LC_ALL, 'portuguese_brazil')

from django.shortcuts import (
	render, redirect, render_to_response, get_list_or_404
	)
from django.contrib.auth import (
    logout as logout_user, login as login_user, authenticate
	)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.models import User
from .models import *
from .forms import *
import json, smtplib, csv, os
from unidecode import unidecode
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email import encoders
from email.message import Message


@login_required(login_url='/login/')
def index(request):
	title = "BulkMail | Index"
	return render(request, "bulkmail/index.html", {'title':title})

@login_required(login_url='/login/')
def send_bulk_mail(request):
	title = "Envio com sucesso!"
	user = UserProfile.objects.get(user=request.user.id)
	if request.method == "POST":
		files = request.FILES.getlist("files[]")
		list_emails = request.POST.getlist("resident_email")
		subject = request.POST["subject"]
		aditional_email = request.POST["aditional_email"]
		if len(aditional_email) > 0:
			list_emails.append(aditional_email)
		if request.POST.get('send_for_me', None):
			list_emails.append(user.email_user)
		message_box = request.POST["message_box"]
		message_box = message_box.replace('\r\n','<br/>')
		COMMASPACE = ', '
		# Create the container (outer) email message.
		msg = MIMEMultipart()
		msg['Subject'] = subject
		# me == the sender's email address
		# family = the list of all recipients' email addresses
		msg['From'] = user.email_user
		msg['To'] = COMMASPACE.join(list_emails)
		msg.preamble = str(subject.encode('utf-8'))
		body_html =  """\
				<html>
				  <head></head>
				  <body>
					{:s}
					<br>
					<br>
					<br>
					<p style="font-size:14px;"><strong>Campagnolli, Ciolfi & Correa Prata Ltda-ME</strong></p>
					<p style="font-size:13px;">Tel.: +55 19 3733.8888</p>
					<a style="font-size:13px;" href="http://www.campagnolli.com.br" title="Campagnolli" target="_blank">http://www.campagnolli.com.br</a>
					<br>
					__________________________________________________________
					<p style="font-size:14px; color:green"><strong><i>Em respeito ao Meio Ambiente imprima este documento somente se necessário!</i></strong></p>
				  </body>
				</html>
				""".format(message_box)
		body_text = message_box
		msg.attach(MIMEText(body_html, 'html', _charset="utf-8"))
		
		for file in files:
			part = MIMEBase('application', "octet-stream")
			part.set_payload(file.read())
			encoders.encode_base64(part)
			part.add_header('Content-Disposition', 'attachment; filename="%s"' % unidecode(file.name))
			msg.attach(part)
			
		# Send the email via our own SMTP server.
		
		server = smtplib.SMTP(user.outgoing_mail_server, user.outgoing_server)
		server.login(user.email_user, user.password_email)
		server.send_message(msg)
		server.quit()
		
		return redirect('/')
	return HttpResponse("Volte!")

@login_required(login_url='/login/')
def add_condominium(request):
	title = "BulkMail | Adicionar condomínios"
	if request.method == "POST":
		condform = CondominiumForm(request.POST)
		if condform.is_valid():
			condform.save()
			return redirect("/add_condominium/")
	else:
		condform = CondominiumForm()
	return render(request, "bulkmail/add_condominium.html", {
			'condform':condform, 'title':title
			})

@login_required(login_url='/login/')
def manage_resident(request):
	title = "BulkMail | Adicionar condôminos"
	if request.method == "POST":
		user = UserProfile.objects.get(user=request.user.id)
		residentform = ResidentForm(request.POST)
		if residentform.is_valid():
			resid = residentform.save(commit=False)
			resid.who_modify = user
			resid.save()
			residentform.save()
			return redirect("manage_resident")
	else:
		residentform = ResidentForm()
	return render(request, "bulkmail/manage_resident.html", {
			'residentform':residentform, 'title':title
			})

@user_passes_test(lambda u: u.is_superuser, login_url="/", redirect_field_name=None)
def manage_users(request):
	title = "BulkMail | Gerenciamento de Usuários"
	users = UserProfile.objects.all().order_by('email_user')
	if request.method == "POST":
		userform = UserForm(request.POST)
		userprofile_form = UserProfileForm(request.POST)
		if userform.is_valid():
			email_user = request.POST["email_user"]
			password_email = request.POST["password_email"]
			new_user = User.objects.create_user(
				username=request.POST["username"],
				password=request.POST["password"],
				is_superuser=request.POST.getlist("is_superuser")
				)
			new_user.save()
			user_obj = User.objects.get(username=request.POST["username"])
			user_profile = UserProfile(
						user=user_obj,
						email_user=email_user,
						password_email=password_email
						)
			user_profile.save()
			return redirect("manage_users")
	else:
		userform = UserForm()
		userprofile_form = UserProfileForm()
	return render(request, "bulkmail/manage_users.html", {
		'title':title, 'userform':userform, 'userprofile_form':userprofile_form, 'users':users
		})

@login_required(login_url='/login/')
def edit_resident(request, value):
	resident = Resident.objects.get(id=value)
	if request.method == "POST":
		if not request.POST.get('exclude_resident', None):
			editresident_form = EditResidentForm(request.POST, instance=resident)
			if editresident_form.is_valid():
				editresident_form.save()
		else:
			Resident.objects.filter(id=value).delete()
		return HttpResponseRedirect("/manage_resident/")
	else:
		editresident_form = EditResidentForm(instance=resident)
	return render(request, "bulkmail/edit_resident.html", {
		'editresident_form':editresident_form, 'value':value
		})

@user_passes_test(lambda u: u.is_superuser, login_url="/", redirect_field_name=None)
def edit_user(request, value):
	user_profile = UserProfile.objects.get(id=value)
	user = User.objects.get(id=user_profile.user_id)
	if request.method == "POST":
		if not request.POST.get('exclude_user', None):
			userform = UserEditForm(request.POST, instance=user)
			userprofile_form = UserProfileForm(request.POST, instance=user_profile)
			if userform.is_valid() and userprofile_form.is_valid():
				userform.save()
				userprofile_form.save()
		else:
			User.objects.filter(id=user_profile.user_id).delete()
		return HttpResponseRedirect("/manage_users/")
	else:
		userform = UserEditForm(instance=user)
		userprofile_form = UserProfileForm(instance=user_profile)
		return render(request, "bulkmail/edit_user.html",
			{'userform':userform, 'userprofile_form':userprofile_form, 'value':value})

@login_required(login_url='/login/')
def change_pwd(request, value):
	user_profile = UserProfile.objects.get(id=value)
	user = User.objects.get(id=user_profile.user_id)
	if request.method == "POST":
		form = ChangePwdForm(request.POST, instance=user)
		if form.is_valid():
			password = request.POST["password"]
			user.set_password(password)
			user.save()			
			return HttpResponseRedirect("/manage_users/")
	else:
		form = ChangePwdForm()
		return render(request, "bulkmail/change_pwd.html", {'form':form, 'value':value})

@login_required(login_url='/login/')
def user_change_pwd(request):
	if request.method == "POST":
		user = request.user
		form = ChangePwdForm(request.POST, instance=user)
		if form.is_valid():
			password = request.POST["password"]
			user.set_password(password)
			user.save()	
			logout_user(request)
			return redirect('login')		
	else:
		form = ChangePwdForm()
		return render(request, "bulkmail/user_change_pwd.html", {'form':form})

@login_required(login_url='/login/')
def codscc(request, value):
	if request.method == "GET":
		code = value
		data = {'condominium':None, 'residents':None}
		cond = get_list_or_404(Condominium, scc_code=code)
		data['condominium'] = serializers.serialize('json', cond)
		resid = Resident.objects.filter(condominium=cond[0].id)
		data['residents'] = serializers.serialize('json', resid)
		return HttpResponse(json.dumps(data), content_type="application/json")

@login_required(login_url='/login/')
def rel_residents(request, value):
	if request.method == "GET":
		data = {}
		resid = Resident.objects.filter(condominium=value).order_by('num_un')
		data['residents'] = serializers.serialize('json', resid)
		return HttpResponse(json.dumps(data), content_type="application/json")

@login_required(login_url='/login/')
def list_condominium(request):
	if request.method == "GET":
		data = {'condominium':None}
		cond = Condominium.objects.order_by('name_condominium')
		data['condominium'] = serializers.serialize('json', cond)
		return HttpResponse(json.dumps(data), content_type="application/json")

@login_required(login_url='/login/')
def load_from_file(request):
	title = "BulkMail | Carregamento por arquivo"
	if request.method == "POST":
		id_cond = request.POST["condominium"]
		cond = Condominium.objects.get(id=id_cond)
		user = UserProfile.objects.get(user=request.user.id)
		csvfile = request.FILES["files[]"]
		for row in csvfile:
			new_row = str(row.decode("utf-8", "ignore")).split(';')
			
			if len(new_row[1]) > 10 and len(new_row[2]) > 10:
				#print("Unidade >> ",new_row[0],"Nome >> ",new_row[1]," - E-mail >> ",len(new_row[2]))
				
				obj, created = Resident.objects.update_or_create(
						num_un = new_row[0],
						condominium = cond,
						type_of_resident="P",
						defaults={
							'name_resident':new_row[1],
							'email_resident':new_row[2],
							'who_modify':user
						})
			else:
				Resident.objects.filter(condominium=cond, num_un=new_row[0], type_of_resident="P").delete()

			if len(new_row[3]) > 10 and len(new_row[4]) > 10:
				#print("\nUnidade >> ",new_row[0],"Nome >> ",new_row[3]," - E-mail >> ",len(new_row[4]))
				
				obj, created = Resident.objects.update_or_create(
						num_un = new_row[0],
						condominium = cond,
						type_of_resident = "M",
						defaults={
							'name_resident':new_row[3],
							'email_resident':new_row[4],
							'who_modify':user
						})
			else:
				Resident.objects.filter(condominium=cond, num_un=new_row[0], type_of_resident = "M").delete()

		return HttpResponseRedirect("/load_from_file/")
	else:
		form = LoadFromFileForm()
	return render(request, "bulkmail/load_from_file.html", {
		'title':title, 'form':form
		})

def version(request):
	title = "BulkMail | Notas de versão"
	return render(request, "bulkmail/version.html", {'title':title})

def login(request):
	title = "BulkMail | Login"
	errormsg = False
	if request.method == "POST":
		loginform = LoginForm(request.POST)
		if loginform.is_valid():
			user = authenticate(username=request.POST['username'],
				password=request.POST['password'])
			if user is not None:
				if user.is_active:
					login_user(request, user)
					return redirect('/')
			else:
				errormsg = True
	else:
		loginform = LoginForm()
	return render(request, "bulkmail/login.html", {
		'title':title, 'loginform':loginform, 'errormsg':errormsg
		})

def logout(request):
	logout_user(request)
	return redirect('login')
