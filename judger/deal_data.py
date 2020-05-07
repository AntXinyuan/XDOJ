#!/usr/bin/env python
# coding=utf-8
import json
import logging
import os
import shutil
from judger import config
from judger.run_sql import run_sql_without_return, run_sql


def clean_work_dir(solution_id):
    '''清理work目录，删除临时文件'''
    dir_name = os.path.join(config.work_dir, str(solution_id))
    shutil.rmtree(dir_name)


def get_data_count(test_case_id):
    '''获得测试数据的个数信息'''
    full_path = os.path.join(config.data_dir, str(test_case_id))
    try:
        files = os.listdir(full_path)
    except OSError as e:
        logging.error(e)
        return 0
    count = 0
    for item in files:
        if item.endswith(".in"):
            count += 1
    return count


def update_solution_status(id, info=12):
    update_code_sql = "update submission set status = " + str(info) + " where id = '" + id + "';"
    run_sql_without_return(update_code_sql)


def get_problem_limit(problem_id):
    select_code_sql = "select time_limit, memory_limit, test_case_id from problem where id = " + str(problem_id) + ";"
    return run_sql(select_code_sql)


def update_compile_info(id, info):
    update_code_sql = "update submission set error_info = '" + info + "' where id = '" + id + "';"
    run_sql_without_return(update_code_sql)


'''
program_info = {
        "solution_id": solution_id,
        "problem_id": problem_id,
        "take_time": 0,
        "take_memory": 0,
        "user_id": user_id,
        "result": 0,
    }
'''


def update_solution_result(result):
    statistic_info = {
        "time_cost": result["take_time"],
        "memory_cost": result["take_memory"],
        "score": result["score"]
    }
    update_code_sql = 'update submission set statistic_info = ' + "'" + json.dumps(statistic_info) + "'" + \
                      " where id = '" + result["solution_id"] + "';"
    run_sql_without_return(update_code_sql)
    update_code_sql = "update submission set status = " + str(result["result"]) + \
                      " where id = '" + result["solution_id"] + "';"
    run_sql_without_return(update_code_sql)
