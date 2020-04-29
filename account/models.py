import datetime
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
import account


class User(AbstractUser):
    head_img = models.ImageField('头像', upload_to='head_img', default='/head_img/default.jpg')
    is_confirmed = models.BooleanField('是否激活', default=False)

    class Meta:
        ordering = ['date_joined']
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username

    def make_confirm_string(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        code = make_password(self.username, salt=now)
        account.models.ConfirmString.objects.create(code=code, user=self)
        return code


class ConfirmString(models.Model):
    code = models.CharField('激活码', max_length=256)
    user = models.OneToOneField('User', verbose_name='所属用户', on_delete=models.CASCADE)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.user.username + ":   " + self.code

    class Meta:
        ordering = ["-create_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"
