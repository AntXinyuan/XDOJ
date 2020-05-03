from django.db import models
from account.models import User


class Announcement(models.Model):
    title = models.CharField('标题', max_length=32)
    content = models.TextField('内容', max_length=1024, blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    created_by = models.ForeignKey(User, verbose_name='创建者', on_delete=models.CASCADE)
    last_update_time = models.DateTimeField('上次修改时间', auto_now=True)
    visible = models.BooleanField('是否可见', default=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'announcement'
        verbose_name = '公告'
        verbose_name_plural = '公告'
        ordering = ("-create_time",)
