# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-14 04:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('regiclass', '0005_auto_20170810_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturephoto',
            name='lecture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lecture_photos', to='regiclass.Lecture'),
        ),
    ]
