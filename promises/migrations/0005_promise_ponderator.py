# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promises', '0004_auto_20150828_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='promise',
            name='ponderator',
            field=models.FloatField(default=None, null=True, blank=True),
        ),
    ]
