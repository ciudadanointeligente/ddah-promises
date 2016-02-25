# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promises', '0007_promise_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fulfillment',
            name='percentage',
            field=models.FloatField(default=0),
        ),
    ]
