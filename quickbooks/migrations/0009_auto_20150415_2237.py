# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickbooks', '0008_qbitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseLineAdd',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.CharField(max_length=2500, null=True, blank=True)),
                ('memo', models.CharField(max_length=2500, null=True, blank=True)),
                ('account_ref', models.ForeignKey(blank=True, to='quickbooks.QBAccount', null=True)),
                ('customer_ref', models.ForeignKey(blank=True, to='quickbooks.QBCustomer', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QBBill',
            fields=[
                ('txn_date', models.CharField(max_length=255, null=True, blank=True)),
                ('due_date', models.CharField(max_length=255, null=True, blank=True)),
                ('ref_number', models.CharField(max_length=2500, null=True, blank=True)),
                ('memo', models.CharField(max_length=2500, null=True, blank=True)),
                ('exchange_rate', models.CharField(max_length=2500, null=True, blank=True)),
                ('list_id', models.CharField(max_length=2500, serialize=False, primary_key=True)),
                ('is_pending', models.CharField(max_length=2500, null=True, blank=True)),
                ('edit_sequence', models.CharField(max_length=2500, null=True, blank=True)),
                ('expense_line_add', models.ManyToManyField(to='quickbooks.ExpenseLineAdd', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QBVendor',
            fields=[
                ('name', models.CharField(max_length=2500, null=True, blank=True)),
                ('first_name', models.CharField(max_length=2500, null=True, blank=True)),
                ('middle_name', models.CharField(max_length=2500, null=True, blank=True)),
                ('last_name', models.CharField(max_length=2500, null=True, blank=True)),
                ('full_name', models.CharField(max_length=2500, null=True, blank=True)),
                ('company_name', models.CharField(max_length=2500, null=True, blank=True)),
                ('salutation', models.CharField(max_length=2500, null=True, blank=True)),
                ('job_title', models.CharField(max_length=2500, null=True, blank=True)),
                ('phone', models.CharField(max_length=2500, null=True, blank=True)),
                ('alt_phone', models.CharField(max_length=2500, null=True, blank=True)),
                ('fax', models.CharField(max_length=2500, null=True, blank=True)),
                ('email', models.CharField(max_length=2500, null=True, blank=True)),
                ('contact', models.CharField(max_length=2500, null=True, blank=True)),
                ('alt_contact', models.CharField(max_length=2500, null=True, blank=True)),
                ('notes', models.CharField(max_length=2500, null=True, blank=True)),
                ('account_number', models.CharField(max_length=2500, null=True, blank=True)),
                ('credit_limit', models.CharField(max_length=2500, null=True, blank=True)),
                ('vendor_tax_ident', models.CharField(max_length=2500, null=True, blank=True)),
                ('list_id', models.CharField(max_length=2500, serialize=False, primary_key=True)),
                ('is_pending', models.CharField(max_length=2500, null=True, blank=True)),
                ('edit_sequence', models.CharField(max_length=2500, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='qbbill',
            name='vendor_ref',
            field=models.ForeignKey(blank=True, to='quickbooks.QBVendor', null=True),
            preserve_default=True,
        ),
    ]
