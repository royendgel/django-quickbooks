# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickbooks', '0001_squashed_0017_qbitem_sales_or_purchase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messageque',
            name='last_accessed',
            field=models.TimeField(auto_now=True),
            preserve_default=True,
        ),
    ]
