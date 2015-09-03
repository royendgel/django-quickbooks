# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickbooks', '0012_auto_20150421_1705'),
    ]

    operations = [
        migrations.CreateModel(
            name='QBItemPayment',
            fields=[
                ('list_id', models.CharField(max_length=2500, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('item_desc', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
