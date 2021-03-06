# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-08 18:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Condominium',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scc_code', models.PositiveSmallIntegerField(verbose_name='Código SCC')),
                ('name_condominium', models.CharField(max_length=200, verbose_name='Nome do condomínio')),
            ],
        ),
        migrations.CreateModel(
            name='Resident',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_un', models.CharField(max_length=25, verbose_name='Número da unidade')),
                ('type_of_resident', models.CharField(choices=[('P', 'Proprietário'), ('M', 'Morador')], max_length=1, verbose_name='Tipo')),
                ('name_resident', models.CharField(max_length=200, verbose_name='Nome do condômino')),
                ('email_resident', models.EmailField(max_length=254, verbose_name='E-mail do condômino')),
                ('last_modified', models.DateField(default=django.utils.timezone.now)),
                ('condominium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bulkmail.Condominium', verbose_name='Condomínio')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_user', models.CharField(max_length=100, verbose_name='E-mail')),
                ('password_email', models.CharField(max_length=100, verbose_name='Senha do e-mail')),
                ('outgoing_mail_server', models.CharField(default='mail.campagnolli.com.br', max_length=100)),
                ('outgoing_server', models.PositiveSmallIntegerField(default=587)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='resident',
            name='who_modify',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bulkmail.UserProfile'),
        ),
    ]
