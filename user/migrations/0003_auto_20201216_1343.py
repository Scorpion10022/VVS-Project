# Generated by Django 3.1.4 on 2020-12-16 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_profile_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='status',
        ),
    ]
