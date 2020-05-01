# Generated by Django 3.0.3 on 2020-05-01 16:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20200501_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_reset_password_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='上次重置密码时间'),
            preserve_default=False,
        ),
    ]
