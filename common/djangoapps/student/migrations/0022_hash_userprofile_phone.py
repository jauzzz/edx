# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-10 06:17
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth.models import User
from student.hasher import AESCipher

def forwards_func(apps, schema_editor):
    users = User.objects.all()
    hasher = AESCipher
    for user in users:
        user.save()
        user.profile.save()


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0021_auto_20191216_0429'),
    ]

    operations = [
        migrations.RunPython(forwards_func),
    ]
