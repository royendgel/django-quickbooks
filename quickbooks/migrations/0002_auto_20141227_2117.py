# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickbooks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='major_version',
            field=models.CharField(max_length=255, default='', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='minor_version',
            field=models.CharField(max_length=255, default='', blank=True),
            preserve_default=True,
        ),
    ]
