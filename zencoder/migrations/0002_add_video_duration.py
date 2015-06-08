# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zencoder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='duration',
            field=models.PositiveIntegerField(blank=True, default=0),
            preserve_default=True,
        ),
    ]
