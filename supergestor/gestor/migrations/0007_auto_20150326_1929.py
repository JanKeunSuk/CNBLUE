# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0006_auto_20150326_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='email',
            field=models.ForeignKey(to='gestor.Permitido'),
            preserve_default=True,
        ),
    ]
