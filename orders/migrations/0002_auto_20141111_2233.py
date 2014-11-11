# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.CharField(max_length=100, choices=[(b'XS', b'Extra Small Tee'), (b'S', b'Small Tee'), (b'M', b'Medium Tee'), (b'L', b'Large Tee'), (b'XL', b'Extra Large Tee'), (b'XXL', b'Double Extra Large Tee')]),
        ),
    ]
