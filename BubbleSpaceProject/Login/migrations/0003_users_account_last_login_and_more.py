# Generated by Django 5.1.1 on 2024-10-26 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0002_users_account_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='users_account',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AlterField(
            model_name='users_account',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
