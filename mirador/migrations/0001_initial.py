# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_app_lti', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IsiteImages',
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
                ('s3_key', models.CharField(max_length=4096, null=True)),
                ('s3_bucket', models.CharField(max_length=128, null=True)),
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
            name='LTIResourceCollections',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=128)),
                ('sort_order', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'verbose_name': 'LTI Resource Collection',
                'verbose_name_plural': 'LTI Resource Collections',
            },
        ),
        migrations.CreateModel(
            name='LTIResourceImages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('collection', models.ForeignKey(to='mirador.LTIResourceCollections', null=True)),
                ('isite_image', models.ForeignKey(to='mirador.IsiteImages')),
                ('resource', models.ForeignKey(to='django_app_lti.LTIResource')),
            ],
            options={
                'verbose_name': 'LTI Resource Images',
                'verbose_name_plural': 'LTI Resource Images',
            },
        ),
    ]
