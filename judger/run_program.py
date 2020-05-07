#!/usr/bin/env python
# coding=utf-8
import logging

from judger.check_dangerout_code import check_dangerous_code
from judger.compiler import compiler
from judger.deal_data import get_problem_limit, get_data_count
from judger.judge_main import judge
from judger.protect import low_level, dblock

def run(problem_id, solution_id, language, user_id):
    low_level()
    '''获取程序执行时间和内存'''
    dblock.acquire()
    data = get_problem_limit(problem_id)
    print(data)
    time_limit, mem_limit, test_case_id = data[0][0], data[0][1], data[0][2]
    data_count = get_data_count(test_case_id)  # 获取测试数据的个数
    dblock.release()
    program_info = {
        "solution_id": solution_id,
        "problem_id": problem_id,
        "take_time": 0,
        "take_memory": 0,
        "user_id": user_id,
        "result": 0,
        "score": 0,
    }
    result_code = {
        "Waiting": 0,
        "Accepted": 1,
        "Time Limit Exceeded": 2,
        "Memory Limit Exceeded": 3,
        "Wrong Answer": 4,
        "Runtime Error": 5,
        "Output limit": 6,
        "Compile Error": 7,
        "Presentation Error": 8,
        "System Error": 11,
        "Judging": 12,
    }
    if check_dangerous_code(solution_id, language) is False:
        program_info['result'] = result_code["Runtime Error"]
        return program_info
    compile_result = compiler(solution_id, language)
    if compile_result is False:  # 编译错误
        program_info['result'] = result_code["Compile Error"]
        return program_info
    if data_count == 0:  # 没有测试数据
        program_info['result'] = result_code["System Error"]
        return program_info
    result = judge(
        solution_id,
        test_case_id,
        data_count,
        time_limit,
        mem_limit,
        program_info,
        result_code,
        language)
    logging.debug(result)
    return result
