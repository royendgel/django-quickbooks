# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quickbooks', '0008_qbitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='DjangoUserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('company_file', models.CharField(default='', max_length=2500, blank=True)),
                ('major_version', models.CharField(default='', max_length=2500, blank=True)),
                ('minor_version', models.CharField(default='', max_length=2500, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
        migrations.AlterField(
            model_name='messageque',
            name='name',
            field=models.CharField(default='Query', max_length=2500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='receiveresponse',
            name='name',
            field=models.CharField(default='', null=True, max_length=2500, blank=True),
            preserve_default=True,
        ),
    ]
