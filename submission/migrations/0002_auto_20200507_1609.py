# Generated by Django 3.0.6 on 2020-05-07 16:09

from django.db import migrations
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='statistic_info',
            field=django_mysql.models.JSONField(default=dict),
        ),
    ]
