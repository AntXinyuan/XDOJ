import datetime
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone

import account
from django.utils.translation import gettext_lazy as _

from XDOJ import settings
from utils.tools import rand_str


class Role(models.TextChoices):
    ADMIN = 'Admin', _('管理员')
    ORDINARY = 'Ordinary', _('普通用户')


class MyUserManager(UserManager):
    def create(self, **kwargs):
        user = super().create(**kwargs)
        user.set_password(user.password)
        user.save()
        Profile.objects.create(user=user)
        return user

    def update(self, **kwargs):
        user = super().update(**kwargs)
        if kwargs.get('password', None):
            raw_password = kwargs['password']
            user.set_password(raw_password)
            user.save()
        return user


class User(AbstractUser):
    role = models.TextField(choices=Role.choices, default=Role.ORDINARY)
    head_img = models.ImageField('头像', upload_to='head_img', default='/head_img/default.jpg')
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    last_reset_password_time = models.DateTimeField("上次重置密码时间", auto_now_add=True)
    is_confirmed = models.BooleanField('是否激活', default=False)

    objects = MyUserManager()

    class Meta:
        ordering = ['date_joined']
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username

    def is_super_admin(self):
        return self.is_staff

    def is_oj_admin(self):
        return self.role == Role.ORDINARY

    def is_admin(self):
        return self.is_staff or self.role == Role.ORDINARY

    def make_confirm_string(self):
        code = rand_str()
        account.models.ConfirmString.objects.create(code=code, user=self)
        return code

    def has_reset_password_today(self):
        return timezone.now() < self.last_reset_password_time + datetime.timedelta(days=1)

    def record_reset_password_time(self):
        self.last_reset_password_time = timezone.now()
        self.save()


class ConfirmString(models.Model):
    code = models.CharField('激活码', max_length=256)
    user = models.ForeignKey(to='User', verbose_name='所属用户', on_delete=models.CASCADE)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.user.username + ":   " + self.code

    class Meta:
        ordering = ["-create_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"

    def is_expired(self):
        return timezone.now() > self.create_time + datetime.timedelta(minutes=settings.CONFIRM_MINUTES)


class Profile(models.Model):
    user = models.OneToOneField(to=User, related_name='profile', on_delete=models.CASCADE)
    real_name = models.TextField(null=True)
    blog = models.URLField(null=True)
    github = models.URLField(null=True)
    school = models.TextField(null=True)
    major = models.TextField(null=True)
    accepted_number = models.IntegerField(default=0)
    submission_number = models.IntegerField(default=0)

    class Meta:
        verbose_name = '个人主页'
        verbose_name_plural = '个人主页'
