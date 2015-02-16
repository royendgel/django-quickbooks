# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('quickbooks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='messageque',
            name='last_accessed',
            field=models.TimeField(default=datetime.datetime(2014, 12, 31, 17, 34, 9, 514976, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='receiveresponse',
            name='name',
            field=models.CharField(blank=True, max_length=255, default='', null=True),
            preserve_default=True,
        ),
    ]
