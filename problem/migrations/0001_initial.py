# Generated by Django 3.0.3 on 2020-05-02 20:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


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
                ('name', models.TextField(db_index=True)),
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
                ('title', models.CharField(max_length=32, verbose_name='标题')),
                ('description', models.TextField(max_length=512, verbose_name='问题描述')),
                ('input_description', models.TextField(max_length=512, verbose_name='输入描述')),
                ('output_description', models.TextField(max_length=512, verbose_name='输出描述')),
                ('hint', models.TextField(default='', max_length=512, verbose_name='样例说明')),
                ('samples', jsonfield.fields.JSONField(verbose_name='测试样例')),
                ('time_limit', models.IntegerField(help_text='ms', verbose_name='时间限制')),
                ('memory_limit', models.IntegerField(help_text='MB', verbose_name='内存限制')),
                ('difficulty', models.IntegerField(choices=[(1, 'Low'), (2, 'Mid'), (3, 'High')], verbose_name='难度')),
                ('languages', jsonfield.fields.JSONField(verbose_name='编程语言')),
                ('is_public', models.BooleanField(default=True, verbose_name='是否公开')),
                ('visible', models.BooleanField(default=True, verbose_name='是否可见')),
                ('share_submission', models.BooleanField(default=False, verbose_name='是否分享提交')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('last_update_time', models.DateTimeField(auto_now=True, verbose_name='上次修改时间')),
                ('test_case_scores', jsonfield.fields.JSONField(verbose_name='测试点')),
                ('judge_mode', models.TextField(choices=[('Stardand', '标准'), ('Cumulative', '累加')], default='Stardand', verbose_name='评判模式')),
                ('total_score', models.IntegerField(default=0, verbose_name='总分')),
                ('submission_number', models.BigIntegerField(default=0, verbose_name='提交数')),
                ('accepted_number', models.BigIntegerField(default=0, verbose_name='通过数')),
                ('statistic_info', jsonfield.fields.JSONField(verbose_name='统计信息')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
                ('tags', models.ManyToManyField(blank=True, db_table='problem_tag_problem', related_name='problems', to='problem.ProblemTag', verbose_name='标签')),
            ],
            options={
                'verbose_name': '题目',
                'verbose_name_plural': '题目',
                'db_table': 'problem',
                'ordering': ['id', 'difficulty'],
            },
        ),
    ]
