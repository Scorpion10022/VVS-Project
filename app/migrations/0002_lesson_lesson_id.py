# Generated by Django 3.1.2 on 2020-10-22 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='lesson_id',
            field=models.IntegerField(default=1),
        ),
    ]
