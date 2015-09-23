# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promises', '0005_promise_ponderator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='informationsource',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='verificationdocument',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
