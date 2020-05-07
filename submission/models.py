from django.db import models
from django_mysql.models import JSONField
from account.models import User
from judger.judger import JudgeStatus
from utils.tools import rand_str
from problem.models import Problem


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
    status = models.IntegerField(choices=JudgeStatus.choices, default=JudgeStatus.WAITING, db_index=True)
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

    @staticmethod
    def update_all_statistic_info(id):
        submission = Submission.objects.get(id=id)
        problem = submission.problem
        user_profile = submission.user.profile

        status = submission.status
        status_dict = JudgeStatus.dict()

        problem.submission_number += 1
        user_profile.submission_number += 1
        if status == JudgeStatus.ACCEPTED:
            problem.accepted_number += 1
            user_profile.accepted_number += 1
            problem.statistic_info[status_dict[submission.status]] += 1
        elif status == JudgeStatus.WAITING or status == JudgeStatus.JUDGING:
            pass
        else:
            problem.statistic_info[status_dict[submission.status]] += 1

        problem.save()
        user_profile.save()
