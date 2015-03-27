# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0004_remove_hu_proyecto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permitido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=255, verbose_name=b'email address')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='hu',
            name='kanban',
        ),
        migrations.RemoveField(
            model_name='hu',
            name='sprint',
        ),
    ]
