"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
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
	url(r'^login/$', views.login, name='login'),
	url(r'^logout', views.logout, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
