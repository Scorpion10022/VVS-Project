# Generated by Django 3.1.2 on 2020-10-30 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20201030_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_title',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
