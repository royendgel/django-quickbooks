# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageQue',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=255, default='Query')),
                ('description', models.TextField(blank=True, null=True)),
                ('message', models.TextField()),
                ('active', models.BooleanField(default=True)),
                ('repeat', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QBCustomer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('notes', models.CharField(blank=True, max_length=255, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=255, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('fax', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('contact', models.CharField(blank=True, max_length=255, null=True)),
                ('account_number', models.CharField(blank=True, max_length=255, null=True)),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('ship_address', models.CharField(blank=True, max_length=255, null=True)),
                ('sublevel', models.CharField(blank=True, max_length=255, null=True)),
                ('alt_phone', models.CharField(blank=True, max_length=255, null=True)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('customer_type_ref', models.CharField(blank=True, max_length=255, null=True)),
                ('total_balance', models.CharField(blank=True, max_length=255, null=True)),
                ('bill_address', models.CharField(blank=True, max_length=255, null=True)),
                ('addr2', models.CharField(blank=True, max_length=255, null=True)),
                ('item_sales_tax_ref', models.CharField(blank=True, max_length=255, null=True)),
                ('alt_contact', models.CharField(blank=True, max_length=255, null=True)),
                ('addr4', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.CharField(blank=True, max_length=255, null=True)),
                ('addr3', models.CharField(blank=True, max_length=255, null=True)),
                ('list_id', models.CharField(blank=True, max_length=255, null=True)),
                ('addr1', models.CharField(blank=True, max_length=255, null=True)),
                ('job_status', models.CharField(blank=True, max_length=255, null=True)),
                ('edit_sequence', models.CharField(blank=True, max_length=255, null=True)),
                ('time_created', models.CharField(blank=True, max_length=255, null=True)),
                ('time_modified', models.CharField(blank=True, max_length=255, null=True)),
                ('sales_tax_code_ref', models.CharField(blank=True, max_length=255, null=True)),
                ('balance', models.CharField(blank=True, max_length=255, null=True)),
                ('terms_ref', models.CharField(blank=True, max_length=255, null=True)),
                ('salutation', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QWCTicket',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('ticket', uuidfield.fields.UUIDField(blank=True, editable=False, unique=True, max_length=32)),
                ('active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReceiveResponse',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('response', models.TextField()),
                ('processed', models.BooleanField(default=False)),
                ('ticket', models.ForeignKey(to='quickbooks.QWCTicket')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('company_file', models.CharField(blank=True, max_length=255, default='')),
                ('major_version', models.CharField(blank=True, max_length=255, default='')),
                ('minor_version', models.CharField(blank=True, max_length=255, default='')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
