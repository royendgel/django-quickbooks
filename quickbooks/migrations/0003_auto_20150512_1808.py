# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickbooks', '0002_auto_20150430_2033'),
    ]

    operations = [
        migrations.CreateModel(
            name='QWCMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('request_type', models.CharField(max_length=255, choices=[(b'closeConnection', b'Close Connection'), (b'authenticate', b'Authenticate'), (b'receiveResponseXML', b'Receive Request'), (b'sendRequestXML', b'Send Request'), (b'connectionError', b'Connection Error'), (b'getInteractiveUrl', b'Get Interactive URL'), (b'getLastError', b'Get Last Error'), (b'serverVersion', b'Server Version'), (b'clientVersion', b'Client Version')])),
                ('description', models.TextField(null=True, blank=True)),
                ('message', models.TextField(null=True, blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResponseError',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status_code', models.PositiveIntegerField()),
                ('content', models.TextField(null=True, blank=True)),
                ('reason_phrase', models.TextField(null=True, blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('processed', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='qbbill',
            name='txn_id',
            field=models.CharField(max_length=255, serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
