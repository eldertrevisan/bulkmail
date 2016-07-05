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

from django import forms
from .models import *
from django.contrib.auth.models import User


class LoginForm(forms.Form):
	username = forms.CharField(
						widget=forms.widgets.TextInput,
						label="Username"
						)
	password = forms.CharField(
						widget=forms.widgets.PasswordInput,
                        label="Senha"
						)
	class Meta:
		fields = ['username','password']

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.fields["username"].widget.attrs['autofocus'] = 'autofocus'


class UserForm(forms.ModelForm):
	password = forms.CharField(
						widget=forms.widgets.PasswordInput,
                        label="Senha"
						)
	class Meta:
		model = User
		fields = ["username", "password", "is_superuser"]

	def __init__(self, *args, **kwargs):
		super(UserForm, self).__init__(*args, **kwargs)
		self.fields["username"].widget.attrs['autofocus'] = 'autofocus'


class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ["username", "is_superuser"]

	def __init__(self, *args, **kwargs):
		super(UserEditForm, self).__init__(*args, **kwargs)
		self.fields["username"].widget.attrs['autofocus'] = 'autofocus'


class UserProfileForm(forms.ModelForm):
	email_user = forms.EmailField(
						widget=forms.widgets.TextInput,
						label="E-mail",
						max_length=254
						)
	password_email = forms.CharField(
						widget=forms.widgets.TextInput, 
						label="Senha do e-mail",
						max_length=50
						)
	outgoing_mail_server = forms.CharField(
						widget=forms.widgets.TextInput,
						label="Servidor SMTP (Deixar em branco se não souber)",
						max_length=254,
						required=False
						)
	outgoing_server = forms.IntegerField(
						label="Servidor de saída SMTP (Deixar em branco se não souber)",
						required=False
						)
    
	class Meta:
		model = UserProfile
		fields = []


class ChangePwdForm(forms.ModelForm):
	password = forms.CharField(
						widget=forms.widgets.PasswordInput,
                        label="Nova senha",
						required=True
						)
	class Meta:
		model = User
		fields = ["password"]

	def __init__(self, *args, **kwargs):
		super(ChangePwdForm, self).__init__(*args, **kwargs)
		self.fields["password"].widget.attrs['autofocus'] = 'autofocus'


class CondominiumForm(forms.ModelForm):
	class Meta:
		model = Condominium
		fields = ["scc_code", "name_condominium"]

	def __init__(self, *args, **kwargs):
		super(CondominiumForm, self).__init__(*args, **kwargs)
		self.fields["scc_code"].widget.attrs['autofocus'] = 'autofocus'

class ResidentForm(forms.ModelForm):
	class Meta:
		model = Resident
		fields = ["condominium", "type_of_resident", "num_un", "name_resident",\
			"email_resident"]

	def __init__(self, *args, **kwargs):
		super(ResidentForm, self).__init__(*args, **kwargs)
		self.fields["condominium"].widget.attrs['autofocus'] = 'autofocus'
		self.fields['condominium'].queryset = Condominium.objects.order_by('name_condominium')


class EditResidentForm(forms.ModelForm):
	exclude_resident = forms.BooleanField(
							widget=forms.widgets.CheckboxInput,
							label="Excluir condômino",
							required=False)
	class Meta:
		model = Resident
		fields = ["condominium", "type_of_resident", "num_un", "name_resident",\
			"email_resident", "exclude_resident"]


class LoadFromFileForm(forms.ModelForm):
	class Meta:
		model = Resident
		fields = ['condominium']
		
	def __init__(self, *args, **kwargs):
		super(LoadFromFileForm, self).__init__(*args, **kwargs)
		self.fields['condominium'].queryset = Condominium.objects.order_by('name_condominium')