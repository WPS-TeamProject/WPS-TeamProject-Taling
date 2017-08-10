# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-10 05:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('regiclass', '0004_merge_20170810_1429'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-modify_date']},
        ),
        migrations.AlterField(
            model_name='review',
            name='lecture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='regiclass.Lecture'),
        ),
    ]
