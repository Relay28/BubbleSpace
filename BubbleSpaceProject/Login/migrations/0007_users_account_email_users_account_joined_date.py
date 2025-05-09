# Generated by Django 5.1.3 on 2024-12-01 08:50

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0006_alter_users_account_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='users_account',
            name='email',
            field=models.EmailField(default=1, max_length=254, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='users_account',
            name='joined_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
