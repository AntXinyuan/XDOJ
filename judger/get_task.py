#!/usr/bin/env python
# coding=utf-8
import logging
from judger.deal_data import update_solution_status
from judger.get_code import get_code
from judger.protect import dblock
from judger.run_sql import run_sql


def get_task(id):
    sql = "select problem_id,user_id,language from submission where id = '" + str(id) + "';"
    # 返回数据库类型的数据
    data = run_sql(sql)
    if data is not None:
        try:
            problem, user, language = data[0][0], data[0][1], data[0][2]
        except :
            logging.error("1 cannot get task of id %s" % id)
            return False
    else:
        logging.error("2 cannot get task of id %s" % id)
        return False

    dblock.acquire()
    ret = get_code(id, problem, language)
    dblock.release()

    if not ret:
        dblock.acquire()
        update_solution_status(id, 11)  #System Error
        dblock.release()
        return False
    task = {
        "solution_id": id,
        "problem_id": problem,
        "user_id": user,
        "pro_lang": language,
    }
    dblock.acquire()
    update_solution_status(id)
    dblock.release()
    return task
