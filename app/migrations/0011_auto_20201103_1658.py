# Generated by Django 3.1.2 on 2020-11-03 16:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20201030_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='date_posted',
            field=models.DateField(blank=True, default=datetime.date(2020, 11, 3)),
        ),
    ]
