# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickbooks', '0004_delete_l'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qbcustomer',
            name='list_id',
            field=models.CharField(max_length=255, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
