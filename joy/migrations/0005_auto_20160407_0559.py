# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-07 05:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('joy', '0004_auto_20160406_2319'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ('date_created',)},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('date_joined',)},
        ),
        migrations.RenameField(
            model_name='user',
            old_name='joined',
            new_name='date_joined',
        ),
        migrations.RemoveField(
            model_name='group',
            name='created',
        ),
        migrations.AddField(
            model_name='group',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 4, 7, 5, 59, 52, 729526, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='membership',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='joy.Group'),
        ),
        migrations.AddField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='joy.User'),
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(through='joy.Membership', to='joy.User'),
        ),
    ]
