# Generated by Django 3.0.3 on 2020-04-29 16:48

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
            options={
                'verbose_name': '题目标签',
                'verbose_name_plural': '题目标签',
                'db_table': 'problem_tag',
            },
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(verbose_name='标题')),
                ('description', models.TextField(verbose_name='问题描述')),
                ('input_description', models.TextField(verbose_name='输入描述')),
                ('output_description', models.TextField(verbose_name='输出描述')),
                ('hint', models.TextField(default='', verbose_name='提示')),
                ('samples', django.contrib.postgres.fields.jsonb.JSONField(verbose_name='测试样例')),
                ('time_limit', models.IntegerField(help_text='ms', verbose_name='时间限制')),
                ('memory_limit', models.IntegerField(help_text='MB', verbose_name='内存限制')),
                ('difficulty', models.IntegerField(choices=[(1, 'Low'), (2, 'Mid'), (3, 'High')], verbose_name='难度')),
                ('languages', django.contrib.postgres.fields.jsonb.JSONField(verbose_name='编程语言')),
                ('is_public', models.BooleanField(default=False, verbose_name='是否公开')),
                ('visible', models.BooleanField(default=True, verbose_name='是否可见')),
                ('share_submission', models.BooleanField(default=False, verbose_name='是否分享提交')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('last_update_time', models.DateTimeField(auto_now=True, verbose_name='上次修改时间')),
                ('test_case_scores', django.contrib.postgres.fields.jsonb.JSONField(verbose_name='测试点')),
                ('judge_mode', models.TextField(choices=[('Stardand', '标准'), ('cumulative', '累加')], default='Stardand', verbose_name='评判模式')),
                ('total_score', models.IntegerField(default=0, verbose_name='总分')),
                ('submission_number', models.BigIntegerField(default=0, verbose_name='提交数')),
                ('accepted_number', models.BigIntegerField(default=0, verbose_name='通过数')),
                ('statistic_info', django.contrib.postgres.fields.jsonb.JSONField(verbose_name='统计信息')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
                ('tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='problem.ProblemTag', verbose_name='标签')),
            ],
            options={
                'verbose_name': '题目',
                'verbose_name_plural': '题目',
                'db_table': 'problem',
            },
        ),
    ]
