from jsonfield import JSONField
from django.db import models
from account.models import User
from django.utils.translation import gettext_lazy as _

Difficulty = models.IntegerChoices('Difficulty', 'Low Mid High')


class JudgeMode(models.TextChoices):
    standard = 'Stardand', _('标准')
    cumulative = 'cumulative', _('累加')


class ProblemTag(models.Model):
    name = models.TextField()

    class Meta:
        db_table = "problem_tag"
        verbose_name = '题目标签'
        verbose_name_plural = '题目标签'

    def __str__(self):
        return self.name


class Problem(models.Model):
    title = models.TextField('标题')
    description = models.TextField('问题描述')
    input_description = models.TextField('输入描述')
    output_description = models.TextField('输出描述')
    hint = models.TextField('提示', default='')
    # [{input: "test", output: "123"}, {input: "test123", output: "456"}]
    samples = JSONField(verbose_name='测试样例')

    time_limit = models.IntegerField('时间限制', help_text='ms')
    memory_limit = models.IntegerField('内存限制', help_text='MB')
    difficulty = models.IntegerField('难度', choices=Difficulty.choices)
    # ["c++", "java", "python"]
    languages = JSONField(verbose_name='编程语言')
    tags = models.ManyToManyField(to=ProblemTag, verbose_name='标签', related_name='problems',
                                  db_table='problem_tag_problem', blank=True, null=True)

    is_public = models.BooleanField('是否公开', default=True)
    visible = models.BooleanField('是否可见', default=True)
    share_submission = models.BooleanField('是否分享提交', default=False)

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_update_time = models.DateTimeField('上次修改时间', auto_now=True)
    created_by = models.ForeignKey(to=User, verbose_name='创建者', on_delete=models.CASCADE)

    # [{"input_name": "1.in", "output_name": "1.out", "score": 0}]
    test_case_scores = JSONField(verbose_name='测试点')
    judge_mode = models.TextField('评判模式', choices=JudgeMode.choices, default=JudgeMode.standard)
    total_score = models.IntegerField('总分', default=0)

    submission_number = models.BigIntegerField('提交数', default=0)
    accepted_number = models.BigIntegerField('通过数', default=0)
    # {JudgeStatus.ACCEPTED: 3, JudgeStaus.WRONG_ANSWER: 11}
    statistic_info = JSONField(verbose_name='统计信息')

    class Meta:
        db_table = 'problem'
        ordering = ['id', 'difficulty']
        verbose_name = '题目'
        verbose_name_plural = '题目'

    def __str__(self):
        return '[%04d] %s' % (self.id, self.title)
