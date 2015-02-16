# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickbooks', '0003_l_qbaccount_qbcheck_qbestimate_qbinvoice'),
    ]

    operations = [
        migrations.DeleteModel(
            name='L',
        ),
    ]
