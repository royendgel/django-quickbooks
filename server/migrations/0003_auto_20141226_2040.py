# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_qwcticket_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qwcticket',
            name='ticket',
            field=uuidfield.fields.UUIDField(editable=False, blank=True, unique=True, max_length=32),
            preserve_default=True,
        ),
    ]
