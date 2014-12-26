# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_auto_20141226_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='qwcticket',
            name='company_file',
            field=models.CharField(blank=True, max_length=255, default=''),
            preserve_default=True,
        ),
    ]
