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

from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from bulkmail import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^$', views.index, name='index'),
	url(r'^send_bulk_mail/$', views.send_bulk_mail, name='send_bulk_mail'),
	url(r'^add_condominium/$', views.add_condominium, name='add_condominium'),
	url(r'^user_change_pwd/$', views.user_change_pwd, name='user_change_pwd'),
	url(r'^manage_resident/$', views.manage_resident, name='manage_resident'),
	url(r'^manage_resident/edit_resident/(?P<value>[0-9]+)/$', views.edit_resident, name='edit_resident'),
	url(r'^manage_users/$', views.manage_users, name='manage_users'),
	url(r'^manage_users/edit_user/(?P<value>[0-9]+)/$', views.edit_user, name='edit_user'),
	url(r'^manage_users/change_pwd/(?P<value>[0-9]+)/$', views.change_pwd, name='change_pwd'),
	url(r'^codscc/(?P<value>[0-9]+)/$', views.codscc, name='codscc'),
	url(r'^manage_resident/rel_residents/(?P<value>[0-9]+)/$', views.rel_residents, name='rel_residents'),
	url(r'^list_condominium/$', views.list_condominium, name='list_condominium'),
	url(r'^load_from_file/$', views.load_from_file, name='load_from_file'),
	url(r'^version/$', views.version, name='version'),
	url(r'^login/$', views.login, name='login'),
	url(r'^logout', views.logout, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
