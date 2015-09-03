# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickbooks', '0014_auto_20150422_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='qbbill',
            name='is_paid',
            field=models.CharField(max_length=2500, null=True, blank=True),
            preserve_default=True,
        ),
    ]
