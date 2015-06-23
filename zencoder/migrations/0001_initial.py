# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=0, help_text=b'The encoding status', choices=[(0, b'Not started'), (1, b'Complete'), (2, b'In Progress'), (3, b'Failed')])),
                ('job_id', models.IntegerField()),
                ('data', json_field.fields.JSONField(default='null', help_text='Enter a valid JSON object')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('content_type', models.CharField(max_length=100)),
                ('width', models.IntegerField(null=True, blank=True)),
                ('bitrate', models.IntegerField(help_text=b'In kilobits per second', null=True, blank=True)),
            ],
            options={
                'ordering': ('width', 'bitrate'),
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('poster', models.URLField(null=True, blank=True)),
                ('input', models.URLField(null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='source',
            name='video',
            field=models.ForeignKey(related_name='sources', to='zencoder.Video'),
        ),
        migrations.AddField(
            model_name='job',
            name='video',
            field=models.ForeignKey(to='zencoder.Video'),
        ),
    ]
