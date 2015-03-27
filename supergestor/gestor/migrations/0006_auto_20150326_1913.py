# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0005_auto_20150326_1842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permitido',
            name='id',
        ),
        migrations.AlterField(
            model_name='permitido',
            name='email',
            field=models.EmailField(max_length=255, serialize=False, verbose_name=b'email address', primary_key=True),
            preserve_default=True,
        ),
    ]
