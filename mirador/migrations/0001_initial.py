# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_app_lti', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=128)),
                ('description', models.TextField(null=True, blank=True)),
                ('sort_order', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'verbose_name': 'Image Collection',
                'verbose_name_plural': 'Image Collections',
            },
        ),
        migrations.CreateModel(
            name='ImageSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source_type', models.CharField(default=b'FILE', max_length=4, choices=[(b'FILE', b'File'), (b'LINK', b'URL to File')])),
                ('file_name', models.CharField(max_length=2048, null=True, blank=True)),
                ('file_url', models.CharField(max_length=4096, null=True, blank=True)),
                ('title', models.CharField(max_length=2048)),
                ('description', models.TextField(null=True, blank=True)),
                ('metadata', models.TextField(null=True, blank=True)),
                ('iiif_file_id', models.CharField(max_length=4096, null=True, blank=True)),
                ('is_iiif_compatible', models.BooleanField(default=True)),
                ('is_isite_image', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Image Source',
                'verbose_name_plural': 'Image Sources',
            },
        ),
        migrations.CreateModel(
            name='IsiteImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isite_file_type', models.CharField(max_length=64)),
                ('isite_file_name', models.CharField(max_length=2048)),
                ('isite_file_url', models.CharField(max_length=4096)),
                ('isite_file_title', models.CharField(max_length=2048, null=True, blank=True)),
                ('isite_file_description', models.TextField(null=True, blank=True)),
                ('isite_site_title', models.CharField(max_length=4096)),
                ('isite_topic_title', models.CharField(max_length=4096)),
                ('isite_topic_id', models.CharField(max_length=128)),
                ('isite_keyword', models.CharField(max_length=128)),
                ('iiif_file_id', models.CharField(max_length=4096)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Isite Image',
                'verbose_name_plural': 'Isite Images',
            },
        ),
        migrations.CreateModel(
            name='LTIResourceImages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('collection', models.ForeignKey(to='mirador.ImageCollection', null=True)),
                ('image', models.ForeignKey(to='mirador.ImageSource')),
                ('resource', models.ForeignKey(to='django_app_lti.LTIResource')),
            ],
            options={
                'verbose_name': 'LTI Resource Images',
                'verbose_name_plural': 'LTI Resource Images',
            },
        ),
    ]
