# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickbooks', '0013_qbitempayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='qbitempayment',
            name='edit_sequence',
            field=models.CharField(max_length=2500, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='qbitempayment',
            name='time_created',
            field=models.CharField(max_length=2500, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='qbitempayment',
            name='time_modified',
            field=models.CharField(max_length=2500, null=True, blank=True),
            preserve_default=True,
        ),
    ]
