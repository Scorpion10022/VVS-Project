# Generated by Django 3.1.2 on 2020-11-03 17:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20201103_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='date_posted',
            field=models.DateField(blank=True, default=datetime.date(2020, 11, 3)),
        ),
    ]
