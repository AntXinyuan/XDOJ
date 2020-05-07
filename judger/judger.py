import logging
import threading
from django.db import models
from judger.get_task import get_task
from judger.worker import worker


class Judger(threading.Thread):
    def __init__(self, submission_id, on_finished=None, args=None):
        super().__init__()
        self.id = submission_id
        self.fun = on_finished
        self.args = args

    def run(self):
        logging.basicConfig(level=logging.INFO, filename='logging.log',
                            filemode='w', format='%(asctime)s - %(levelname)s : %(message)s', )
        print("start a thread： " + self.name)
        task = get_task(self.id)
        if not task:
            return
        worker(task)
        if self.fun:
            self.fun(**(self.args))
        print("end a thread： " + self.name)

    def judge_async(self):
        self.start()

    def judge_sync(self):
        self.run()


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

    @staticmethod
    def count_dict():
        return {k: 0 for k in JudgeStatus.labels}