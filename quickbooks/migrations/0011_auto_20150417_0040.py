# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickbooks', '0010_qbbill_txn_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='QBInvoiceLineAdd',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('desc', models.CharField(max_length=2500, null=True, blank=True)),
                ('quantity', models.CharField(max_length=2500, null=True, blank=True)),
                ('unit_of_measure', models.CharField(max_length=2500, null=True, blank=True)),
                ('amount', models.CharField(max_length=2500, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='qbinvoice',
            name='invoice_line_add',
            field=models.ManyToManyField(to='quickbooks.QBInvoiceLineAdd', null=True, blank=True),
            preserve_default=True,
        ),
    ]
