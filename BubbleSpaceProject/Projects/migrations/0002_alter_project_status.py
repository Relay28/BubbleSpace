# Generated by Django 5.1.2 on 2024-11-23 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='Status',
            field=models.CharField(choices=[('Ongoing', 'Ongoing'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled'), ('Pending', 'Pending')], max_length=10),
        ),
    ]
