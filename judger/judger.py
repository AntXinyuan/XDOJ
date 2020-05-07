import logging
import threading
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
