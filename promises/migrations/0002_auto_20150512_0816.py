# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promises', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='promise',
            options={'verbose_name': 'Promise', 'verbose_name_plural': 'Promises'},
        ),
    ]
