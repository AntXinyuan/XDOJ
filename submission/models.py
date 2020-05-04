from django.db import models
from jsonfield import JSONField

from account.models import User
from problem.models import Problem
from utils.tools import rand_str


class JudgeStatus(models.IntegerChoices):
    COMPILE_ERROR = -2
    WRONG_ANSWER = -1
    ACCEPTED = 0
    CPU_TIME_LIMIT_EXCEEDED = 1
    REAL_TIME_LIMIT_EXCEEDED = 2
    MEMORY_LIMIT_EXCEEDED = 3
    RUNTIME_ERROR = 4
    SYSTEM_ERROR = 5
    PENDING = 6
    JUDGING = 7
    PARTIALLY_ACCEPTED = 8


class Submission(models.Model):
    id = models.CharField(max_length=64, default=rand_str, primary_key=True, db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    problem = models.ForeignKey(to=Problem, on_delete=models.CASCADE)
    # contest = models.ForeignKey(to=Contest, null=True, on_delete=models.CASCADE)

    language = models.CharField(max_length=10)
    solution = models.TextField()
    is_shared = models.BooleanField(default=False)

    status = models.IntegerField(db_index=True, default=JudgeStatus.PENDING)
    # {test_case: "1", "detail":""}
    error_info = JSONField(default=dict)
    # {time_cost: "", memory_cost: "", score: 0}
    statistic_info = JSONField(default=dict)

    class Meta:
        ordering = ['-create_time']
        verbose_name = '提交'
        verbose_name_plural = '提交'

    def is_really_shared(self):
        return self.problem.share_submission and self.is_shared

