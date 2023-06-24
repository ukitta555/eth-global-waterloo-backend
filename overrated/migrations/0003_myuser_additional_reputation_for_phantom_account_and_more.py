# Generated by Django 4.2.2 on 2023-06-24 20:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overrated', '0002_myuser_public_key_myuser_public_key_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='additional_reputation_for_phantom_account',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='myuser',
            name='last_reputation_bump_for_phantom_account',
            field=models.DateTimeField(default=datetime.datetime(1970, 1, 1, 12, 0)),
        ),
    ]