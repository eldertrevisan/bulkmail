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

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	email_user = models.CharField(verbose_name="E-mail", max_length=100)
	password_email = models.CharField(verbose_name="Senha do e-mail", max_length=100)
	outgoing_mail_server = models.CharField(max_length=100, default="mail.campagnolli.com.br")
	outgoing_server = models.PositiveSmallIntegerField(default=587)
	
	def __str__(self):
		return str(self.user)


class Condominium(models.Model):
	scc_code = models.PositiveSmallIntegerField(verbose_name="Código SCC")
	name_condominium = models.CharField(verbose_name="Nome do condomínio", max_length=200)
	
	def __str__(self):
		return self.name_condominium


class Resident(models.Model):
	TYPE_OF_RESID_CHOICES = (
			('P', 'Proprietário'),
			('M', 'Morador')
			)
	num_un = models.CharField(verbose_name="Número da unidade", max_length=25)
	type_of_resident = models.CharField(max_length=1, choices=TYPE_OF_RESID_CHOICES, verbose_name="Tipo")
	name_resident = models.CharField(verbose_name="Nome do condômino", max_length=200)
	email_resident = models.EmailField(verbose_name="E-mail do condômino", max_length=254)
	condominium = models.ForeignKey('Condominium', on_delete=models.CASCADE, verbose_name="Condomínio")
	last_modified = models.DateField(default=timezone.now)
	who_modify = models.ForeignKey('UserProfile')
	
	def __str__(self):
		return self.name_resident