# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickbooks', '0015_qbbill_is_paid'),
    ]

    operations = [
        migrations.CreateModel(
            name='QBSalesOrPurchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.CharField(max_length=2500, null=True, blank=True)),
                ('account_ref', models.ForeignKey(blank=True, to='quickbooks.QBAccount', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='qbitem',
            name='sales_or_purchase',
        ),
    ]
