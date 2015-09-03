# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickbooks', '0011_auto_20150417_0040'),
    ]

    operations = [
        migrations.CreateModel(
            name='QBEmployee',
            fields=[
                ('list_id', models.CharField(max_length=2500, serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=2500, null=True, blank=True)),
                ('middle_name', models.CharField(max_length=2500, null=True, blank=True)),
                ('last_name', models.CharField(max_length=2500, null=True, blank=True)),
                ('full_name', models.CharField(max_length=2500, null=True, blank=True)),
                ('name', models.CharField(max_length=2500, null=True, blank=True)),
                ('notes', models.CharField(max_length=2500, null=True, blank=True)),
                ('phone', models.CharField(max_length=2500, null=True, blank=True)),
                ('fax', models.CharField(max_length=2500, null=True, blank=True)),
                ('city', models.CharField(max_length=2500, null=True, blank=True)),
                ('contact', models.CharField(max_length=2500, null=True, blank=True)),
                ('account_number', models.CharField(max_length=2500, null=True, blank=True)),
                ('company_name', models.CharField(max_length=2500, null=True, blank=True)),
                ('is_active', models.CharField(max_length=2500, null=True, blank=True)),
                ('edit_sequence', models.CharField(max_length=2500, null=True, blank=True)),
                ('time_created', models.CharField(max_length=2500, null=True, blank=True)),
                ('time_modified', models.CharField(max_length=2500, null=True, blank=True)),
                ('salutation', models.CharField(max_length=2500, null=True, blank=True)),
                ('email', models.CharField(max_length=2500, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QBItemLineAdd',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('serial_number', models.CharField(max_length=255, null=True, blank=True)),
                ('lot_number', models.CharField(max_length=255, null=True, blank=True)),
                ('desc', models.CharField(max_length=255, null=True, blank=True)),
                ('quantity', models.CharField(max_length=255, null=True, blank=True)),
                ('amount', models.CharField(max_length=2500, null=True, blank=True)),
                ('cost', models.CharField(max_length=255, null=True, blank=True)),
                ('unit_of_measure', models.CharField(max_length=255, null=True, blank=True)),
                ('memo', models.CharField(max_length=2500, null=True, blank=True)),
                ('customer_ref', models.ForeignKey(blank=True, to='quickbooks.QBCustomer', null=True)),
                ('item_ref', models.ForeignKey(blank=True, to='quickbooks.QBItem', null=True)),
                ('sales_rep_ref', models.ForeignKey(blank=True, to='quickbooks.QBEmployee', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='qbbill',
            name='item_line_add',
            field=models.ManyToManyField(to='quickbooks.QBItemLineAdd', null=True, blank=True),
            preserve_default=True,
        ),
    ]
