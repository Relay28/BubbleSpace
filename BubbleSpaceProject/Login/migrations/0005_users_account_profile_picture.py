# Generated by Django 5.1.1 on 2024-11-24 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0004_users_account_groups_users_account_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='users_account',
            name='profile_picture',
            field=models.ImageField(default='profile_pictures/default.jpg', upload_to='profile_pictures/'),
        ),
    ]
