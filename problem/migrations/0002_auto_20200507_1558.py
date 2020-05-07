# Generated by Django 3.0.6 on 2020-05-07 15:58

from django.db import migrations
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='languages',
            field=django_mysql.models.JSONField(default=dict, verbose_name='编程语言'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='samples',
            field=django_mysql.models.JSONField(default=dict, verbose_name='测试样例'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='statistic_info',
            field=django_mysql.models.JSONField(default=dict, verbose_name='统计信息'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='test_case_scores',
            field=django_mysql.models.JSONField(default=dict, verbose_name='测试点'),
        ),
    ]
