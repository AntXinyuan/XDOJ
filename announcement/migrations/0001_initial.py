# Generated by Django 3.0.3 on 2020-05-02 12:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(verbose_name='标题')),
                ('content', models.TextField(blank=True, verbose_name='内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('last_update_time', models.DateTimeField(auto_now=True, verbose_name='上次修改时间')),
                ('visible', models.BooleanField(default=True, verbose_name='是否可见')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
            options={
                'verbose_name': '公告',
                'verbose_name_plural': '公告',
                'db_table': 'announcement',
                'ordering': ('-create_time',),
            },
        ),
    ]
