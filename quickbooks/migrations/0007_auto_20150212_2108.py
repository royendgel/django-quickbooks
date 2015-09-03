# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickbooks', '0006_auto_20150211_0408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qbaccount',
            name='id',
        ),
        migrations.RemoveField(
            model_name='qbcheck',
            name='id',
        ),
        migrations.RemoveField(
            model_name='qbcustomer',
            name='id',
        ),
        migrations.RemoveField(
            model_name='qbestimate',
            name='id',
        ),
        migrations.RemoveField(
            model_name='qbinvoice',
            name='id',
        ),
        migrations.AlterField(
            model_name='qbaccount',
            name='list_id',
            field=models.CharField(max_length=2500, serialize=False, primary_key=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='qbcheck',
            name='list_id',
            field=models.CharField(max_length=2500, serialize=False, primary_key=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='qbcustomer',
            name='list_id',
            field=models.CharField(max_length=2500, serialize=False, primary_key=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='qbestimate',
            name='list_id',
            field=models.CharField(max_length=2500, serialize=False, primary_key=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='qbinvoice',
            name='list_id',
            field=models.CharField(max_length=2500, serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
