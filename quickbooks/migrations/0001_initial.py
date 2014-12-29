# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageQue',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('message', models.TextField()),
                ('active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QBCustomer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('state', models.CharField(max_length=255, blank=True, null=True)),
                ('notes', models.CharField(max_length=255, blank=True, null=True)),
                ('postal_code', models.CharField(max_length=255, blank=True, null=True)),
                ('middle_name', models.CharField(max_length=255, blank=True, null=True)),
                ('phone', models.CharField(max_length=255, blank=True, null=True)),
                ('fax', models.CharField(max_length=255, blank=True, null=True)),
                ('city', models.CharField(max_length=255, blank=True, null=True)),
                ('contact', models.CharField(max_length=255, blank=True, null=True)),
                ('account_number', models.CharField(max_length=255, blank=True, null=True)),
                ('full_name', models.CharField(max_length=255, blank=True, null=True)),
                ('company_name', models.CharField(max_length=255, blank=True, null=True)),
                ('name', models.CharField(max_length=255, blank=True, null=True)),
                ('ship_address', models.CharField(max_length=255, blank=True, null=True)),
                ('sublevel', models.CharField(max_length=255, blank=True, null=True)),
                ('alt_phone', models.CharField(max_length=255, blank=True, null=True)),
                ('first_name', models.CharField(max_length=255, blank=True, null=True)),
                ('last_name', models.CharField(max_length=255, blank=True, null=True)),
                ('customer_type_ref', models.CharField(max_length=255, blank=True, null=True)),
                ('total_balance', models.CharField(max_length=255, blank=True, null=True)),
                ('bill_address', models.CharField(max_length=255, blank=True, null=True)),
                ('addr2', models.CharField(max_length=255, blank=True, null=True)),
                ('item_sales_tax_ref', models.CharField(max_length=255, blank=True, null=True)),
                ('alt_contact', models.CharField(max_length=255, blank=True, null=True)),
                ('addr4', models.CharField(max_length=255, blank=True, null=True)),
                ('is_active', models.CharField(max_length=255, blank=True, null=True)),
                ('addr3', models.CharField(max_length=255, blank=True, null=True)),
                ('list_id', models.CharField(max_length=255, blank=True, null=True)),
                ('addr1', models.CharField(max_length=255, blank=True, null=True)),
                ('job_status', models.CharField(max_length=255, blank=True, null=True)),
                ('edit_sequence', models.CharField(max_length=255, blank=True, null=True)),
                ('time_created', models.CharField(max_length=255, blank=True, null=True)),
                ('time_modified', models.CharField(max_length=255, blank=True, null=True)),
                ('sales_tax_code_ref', models.CharField(max_length=255, blank=True, null=True)),
                ('balance', models.CharField(max_length=255, blank=True, null=True)),
                ('terms_ref', models.CharField(max_length=255, blank=True, null=True)),
                ('salutation', models.CharField(max_length=255, blank=True, null=True)),
                ('email', models.CharField(max_length=255, blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QWCTicket',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('ticket', uuidfield.fields.UUIDField(editable=False, max_length=32, blank=True, unique=True)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('response', models.TextField()),
                ('ticket', models.ForeignKey(to='quickbooks.QWCTicket')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('company_file', models.CharField(max_length=255, blank=True, default='')),
                ('major_version', models.CharField(max_length=255, blank=True, default='')),
                ('minor_version', models.CharField(max_length=255, blank=True, default='')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
