from django.db import models
from account.models import User
from problem.models import Problem


class Contest(models.Model):
    title = models.TextField('标题', default='', max_length=50)
    description = models.TextField('描述', default='', max_length=200)
    release_time = models.DateTimeField('开始时间')
    end_time = models.DateTimeField('截止时间')
    duration = models.IntegerField('比赛限时', help_text='min')
    visible = models.BooleanField('是否可见', default=True)
    created_by = models.ForeignKey(to=User, verbose_name='创建者', on_delete=models.CASCADE)
    problem_set = models.ManyToManyField(to=Problem, verbose_name='比赛题目')
    participants = models.ManyToManyField(to=User, verbose_name='参赛者', through='ContestParticipant', related_name='participants_set')

    class Meta:
        db_table = 'contest'
        verbose_name = '比赛'
        verbose_name_plural = '比赛'
        ordering = ("-release_time",)

    def __str__(self):
        return '[%d] %s' % (self.id, self.title)


class ContestParticipant(models.Model):
    participant = models.ForeignKey(to=User, verbose_name='参赛者', on_delete=models.CASCADE)
    participate_to = models.ForeignKey(to=Contest, verbose_name='比赛ID', on_delete=models.CASCADE)
    score = models.IntegerField('得分', default=0)
    taken_time = models.IntegerField('比赛用时', default=5000)

    class Meta:
        db_table = "contest_participant"
        verbose_name = '参赛者'
        verbose_name_plural = '参赛者'



