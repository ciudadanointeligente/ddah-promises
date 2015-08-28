# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promises', '0003_auto_20150828_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promise',
            name='person',
            field=models.ForeignKey(blank=True, to='popolo.Person', null=True),
        ),
    ]
