import datetime
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone

import account

from XDOJ import settings
from utils.tools import rand_str, ImageStorage


class Role(models.TextChoices):
    SUPER_ADMIN = 'SUPER_ADMIN'
    NORMAL_ADMIN = 'NORMAL_ADMIN'
    USER = 'USER'


class MyUserManager(UserManager):
    def create(self, **kwargs):
        user = super().create(**kwargs)
        user.set_password(user.password)
        user.save()
        Profile.objects.create(user=user)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('role', Role.SUPER_ADMIN)
        extra_fields.setdefault('is_confirmed', True)
        superuser = super()._create_user(username, email, password, **extra_fields)
        Profile.objects.create(user=superuser)
        return superuser


class MyPermissionsMixin(models.Model):
    is_staff = models.BooleanField(default=False)
    role = models.TextField(choices=Role.choices, default=Role.USER)

    class Meta:
        abstract = True

    def is_super_admin(self):
        return self.role == Role.SUPER_ADMIN

    def is_normal_admin(self):
        return self.role == Role.NORMAL_ADMIN

    def is_admin(self):
        return self.role == Role.SUPER_ADMIN or self.role == Role.NORMAL_ADMIN

    def has_module_perms(self, app_label):
        return self.is_super_admin()

    def has_perms(self, perm_list, obj=None):
        return self.is_super_admin()

    def has_perm(self, perm, obj=None):
        return self.is_super_admin()


class User(AbstractBaseUser, MyPermissionsMixin):
    username = models.CharField(max_length=20, unique=True, db_index=True,
                                validators=[UnicodeUsernameValidator()],
                                error_messages={'unique': _("该用户名已存在！")})
    email = models.EmailField(unique=True, db_index=True)
    head_img = models.ImageField('头像', upload_to='head_img', default='/head_img/default.jpg', storage=ImageStorage())
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    last_reset_password_time = models.DateTimeField("上次重置密码时间", auto_now_add=True)
    is_confirmed = models.BooleanField('是否激活', default=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ['create_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username

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
    code = models.CharField('激活码', max_length=256, db_index=True)
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

    def increase_accepted_number(self):
        self.accepted_number += 1
        self.save()

    def increase_submission_number(self):
        self.submission_number += 1
        self.save()
