# Generated by Django 3.0.6 on 2020-05-09 18:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('problem', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='', max_length=50, verbose_name='标题')),
                ('description', models.TextField(default='', max_length=200, verbose_name='描述')),
                ('release_time', models.DateTimeField(verbose_name='开始时间')),
                ('end_time', models.DateTimeField(verbose_name='截止时间')),
                ('duration', models.IntegerField(help_text='min', verbose_name='比赛限时')),
                ('visible', models.BooleanField(default=True, verbose_name='是否可见')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
            options={
                'verbose_name': '比赛',
                'verbose_name_plural': '比赛',
                'db_table': 'contest',
                'ordering': ('-release_time',),
            },
        ),
        migrations.CreateModel(
            name='ContestParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0, verbose_name='得分')),
                ('taken_time', models.IntegerField(default=5000, verbose_name='比赛用时')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='参赛者')),
                ('participate_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contest.Contest', verbose_name='比赛ID')),
            ],
            options={
                'verbose_name': '参赛者',
                'verbose_name_plural': '参赛者',
                'db_table': 'contest_participant',
            },
        ),
        migrations.AddField(
            model_name='contest',
            name='participants',
            field=models.ManyToManyField(related_name='participants_set', through='contest.ContestParticipant', to=settings.AUTH_USER_MODEL, verbose_name='参赛者'),
        ),
        migrations.AddField(
            model_name='contest',
            name='problem_set',
            field=models.ManyToManyField(to='problem.Problem', verbose_name='比赛题目'),
        ),
    ]
