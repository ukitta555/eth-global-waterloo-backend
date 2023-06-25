# Generated by Django 4.2.2 on 2023-06-25 03:38

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('overrated', '0004_remove_myuser_public_key_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='last_reputation_bump_for_phantom_account',
            field=models.DateTimeField(default=datetime.datetime(1970, 1, 1, 12, 0, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='TextMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_text', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]