from django.db import models
from jsonfield import JSONField
from account.models import User
from problem.models import Problem
from utils.tools import rand_str


class JudgeStatus(models.IntegerChoices):
    WAITING = 0
    ACCEPTED = 1
    TIME_LIMIT_EXCEEDED = 2
    MEMORY_LIMIT_EXCEEDED = 3
    WRONG_ANSWER = 4
    RUNTIME_ERROR = 6
    COMPILE_ERROR = 7
    PRESENTATION_ERROR = 8
    SYSTEM_ERROR = 11
    JUDGING = 12

    @staticmethod
    def dict():
        return dict(JudgeStatus.choices)


class Submission(models.Model):
    id = models.CharField(max_length=64, default=rand_str, primary_key=True, db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    problem = models.ForeignKey(to=Problem, on_delete=models.CASCADE)
    # contest = models.ForeignKey(to=Contest, null=True, on_delete=models.CASCADE)

    language = models.CharField(max_length=10)
    solution = models.TextField()
    is_shared = models.BooleanField(default=False)

    # status = models.IntField(max_length=20, db_index=True)
    status = models.IntegerField(choices=JudgeStatus.choices, default=JudgeStatus.WAITING,  db_index=True)
    error_info = models.TextField(max_length=1024, default='')
    # {time_cost: "", memory_cost: "", score: 0}
    statistic_info = JSONField(default=dict)

    class Meta:
        db_table = 'submission'
        ordering = ['-create_time']
        verbose_name = '提交'
        verbose_name_plural = '提交'

    def is_really_shared(self):
        return self.problem.share_submission and self.is_shared

