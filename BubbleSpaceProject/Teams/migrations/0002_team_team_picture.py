# Generated by Django 5.1.1 on 2024-11-29 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='team_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]