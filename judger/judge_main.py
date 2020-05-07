#!/usr/bin/env python
# coding=utf-8
import logging
from judger.judge_one import judge_one_mem_time
from judger.judge_result import judge_result
from judger.protect import low_level


def judge(solution_id, test_case_id, data_count, time_limit,
          mem_limit, program_info, result_code, language):
    low_level()
    '''评测编译类型语言'''
    max_mem = 0
    max_time = 0
    if language in ["java", 'python2', 'python3']:
        time_limit = time_limit * 2
        mem_limit = mem_limit * 2
    score = 0
    for i in range(data_count):
        ret = judge_one_mem_time(
            solution_id,
            test_case_id,
            i + 1,
            time_limit + 10,
            mem_limit,
            language)
        if not ret:
            continue
        if ret['result'] == result_code["Runtime Error"]:
            program_info['result'] = result_code["Runtime Error"]
            return program_info
        elif ret['result'] == result_code["Time Limit Exceeded"]:
            program_info['result'] = result_code["Time Limit Exceeded"]
            program_info['take_time'] = time_limit + 10
            return program_info
        elif ret['result'] == result_code["Memory Limit Exceeded"]:
            program_info['result'] = result_code["Memory Limit Exceeded"]
            program_info['take_memory'] = mem_limit
            return program_info
        if max_time < ret["timeused"]:
            max_time = ret['timeused']
        if max_mem < ret['memoryused']:
            max_mem = ret['memoryused']
        result = judge_result(test_case_id, solution_id, i + 1) #得出结果了，与标准结果对比
        if not result:
            continue
        if result == result_code["Wrong Answer"]:
            program_info['result'] = result_code["Wrong Answer"]
            break
        elif result == result_code["Output limit"]:
            program_info['result'] = result_code["Output limit"]
            break
        elif result == result_code['Presentation Error']:
            program_info['result'] = result_code['Presentation Error']
        elif result == result_code['Accepted']:
            if program_info['result'] != result_code['Presentation Error']:
                program_info['result'] = result_code['Accepted']
                score = score + 1
        else:
            logging.error("judge did not get result")
    program_info['take_time'] = max_time
    program_info['take_memory'] = max_mem
    program_info['score'] = score * 1.0 / data_count * 100
    return program_info

