# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('popolo', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Fulfillment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('percentage', models.PositiveIntegerField(default=0)),
                ('status', models.TextField(default=b'', blank=True)),
                ('description', models.TextField(default=b'', blank=True)),
            ],
            options={
                'verbose_name': 'Fulfilment',
                'verbose_name_plural': 'Fulfilments',
            },
        ),
        migrations.CreateModel(
            name='InformationSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('display_name', models.CharField(max_length=512)),
                ('date', models.DateField()),
            ],
            options={
                'verbose_name': 'Information Source',
                'verbose_name_plural': 'Information Sources',
            },
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('description', models.TextField()),
            ],
            options={
                'ordering': ('date',),
                'verbose_name': 'Milestone',
                'verbose_name_plural': 'Milestones',
            },
        ),
        migrations.CreateModel(
            name='Promise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=2048)),
                ('description', models.TextField(blank=True)),
                ('date', models.DateField(null=True, blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('category', models.ForeignKey(related_name='promises', to='promises.Category', null=True)),
                ('person', models.ForeignKey(to='popolo.Person')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Promise',
                'verbose_name_plural': 'Promises',
            },
        ),
        migrations.CreateModel(
            name='VerificationDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('display_name', models.CharField(max_length=512)),
                ('date', models.DateField()),
                ('promise', models.ForeignKey(related_name='verification_documents', to='promises.Promise', null=True)),
            ],
            options={
                'verbose_name': 'Verification Document',
                'verbose_name_plural': 'Verification Documents',
            },
        ),
        migrations.AddField(
            model_name='milestone',
            name='promise',
            field=models.ForeignKey(related_name='milestones', to='promises.Promise'),
        ),
        migrations.AddField(
            model_name='informationsource',
            name='promise',
            field=models.ForeignKey(related_name='information_sources', to='promises.Promise'),
        ),
        migrations.AddField(
            model_name='fulfillment',
            name='promise',
            field=models.OneToOneField(to='promises.Promise'),
        ),
    ]
