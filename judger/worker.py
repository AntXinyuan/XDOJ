#!/usr/bin/env python
# coding=utf-8
import logging

from judger import config
from judger.deal_data import get_data_count, clean_work_dir, update_solution_result
from judger.protect import dblock
from judger.run_program import run


def worker(task):
    '''工作线程，获得评判任务并执行'''
    id = task['solution_id']
    problem_id = task['problem_id']
    language = task['pro_lang']
    user_id = task['user_id']
    logging.info("judging %s" % id)
    result = run(problem_id, id, language, user_id)  # 评判
    logging.info("%s result %s" % (result['solution_id'], result['result']))
    dblock.acquire()
    update_solution_result(result)
    dblock.release()
    if config.auto_clean:  # 清理work目录
        clean_work_dir(result['solution_id'])

