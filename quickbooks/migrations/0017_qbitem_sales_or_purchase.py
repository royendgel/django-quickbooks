# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickbooks', '0016_auto_20150428_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='qbitem',
            name='sales_or_purchase',
            field=models.ForeignKey(blank=True, to='quickbooks.QBSalesOrPurchase', null=True),
            preserve_default=True,
        ),
    ]
