# Generated by Django 3.0.3 on 2020-04-30 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0008_auto_20200430_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='tags',
            field=models.ManyToManyField(blank=True, db_table='problem_tag_problem', related_name='problems', to='problem.ProblemTag', verbose_name='标签'),
        ),
    ]