# Generated by Django 4.2.2 on 2023-06-24 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('overrated', '0003_myuser_additional_reputation_for_phantom_account_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='myuser',
            name='public_key_length',
        ),
    ]
