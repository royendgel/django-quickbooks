# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickbooks', '0007_auto_20150212_2108'),
    ]

    operations = [
        migrations.CreateModel(
            name='QBItem',
            fields=[
                ('item_desc', models.CharField(max_length=2500, null=True, blank=True)),
                ('item_group_line', models.CharField(max_length=2500, null=True, blank=True)),
                ('sales_tax_code_ref', models.CharField(max_length=2500, null=True, blank=True)),
                ('edit_sequence', models.CharField(max_length=2500, null=True, blank=True)),
                ('average_cost', models.CharField(max_length=2500, null=True, blank=True)),
                ('tax_vendor_ref', models.CharField(max_length=2500, null=True, blank=True)),
                ('tax_rate', models.CharField(max_length=2500, null=True, blank=True)),
                ('quantity_on_order', models.CharField(max_length=2500, null=True, blank=True)),
                ('sales_and_purchase', models.CharField(max_length=2500, null=True, blank=True)),
                ('purchase_cost', models.CharField(max_length=2500, null=True, blank=True)),
                ('list_id', models.CharField(max_length=2500, serialize=False, primary_key=True)),
                ('cogs_account_ref', models.CharField(max_length=2500, null=True, blank=True)),
                ('discount_rate_percent', models.CharField(max_length=2500, null=True, blank=True)),
                ('reorder_point', models.CharField(max_length=2500, null=True, blank=True)),
                ('purchase_desc', models.CharField(max_length=2500, null=True, blank=True)),
                ('pref_vendor_ref', models.CharField(max_length=2500, null=True, blank=True)),
                ('quantity_on_sales_order', models.CharField(max_length=2500, null=True, blank=True)),
                ('name', models.CharField(max_length=2500, null=True, blank=True)),
                ('sublevel', models.CharField(max_length=2500, null=True, blank=True)),
                ('income_account_ref', models.CharField(max_length=2500, null=True, blank=True)),
                ('quantity_on_hand', models.CharField(max_length=2500, null=True, blank=True)),
                ('discount_rate', models.CharField(max_length=2500, null=True, blank=True)),
                ('sales_or_purchase', models.CharField(max_length=2500, null=True, blank=True)),
                ('account_ref', models.CharField(max_length=2500, null=True, blank=True)),
                ('is_print_items_in_group', models.CharField(max_length=2500, null=True, blank=True)),
                ('time_created', models.CharField(max_length=2500, null=True, blank=True)),
                ('sales_desc', models.CharField(max_length=2500, null=True, blank=True)),
                ('asset_account_ref', models.CharField(max_length=2500, null=True, blank=True)),
                ('time_modified', models.CharField(max_length=2500, null=True, blank=True)),
                ('parent_ref', models.CharField(max_length=2500, null=True, blank=True)),
                ('full_name', models.CharField(max_length=2500, null=True, blank=True)),
                ('sales_price', models.CharField(max_length=2500, null=True, blank=True)),
                ('is_active', models.CharField(max_length=2500, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
