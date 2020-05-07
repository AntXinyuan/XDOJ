#!/usr/bin/env python
# coding=utf-8
import os
import lorun
import shlex
import logging

from judger import config
from judger.protect import low_level
import judger.config


def judge_one_mem_time(id, test_case_id, data_num, time_limit, mem_limit, language):
    low_level()
    '''评测一组数据'''
    input_path = os.path.join(config.data_dir, str(test_case_id), '%s.in' % data_num)
    try:
        input_data = open(input_path)
    except:
        return False
    output_path = os.path.join(config.work_dir, id, 'out%s.txt' % data_num)
    temp_out_data = open(output_path, 'w')
    if language == 'java':
        cmd = 'java -cp %s Main' % (os.path.join(config.work_dir, id))
        main_exe = shlex.split(cmd)
    elif language == 'python2':
        cmd = 'python2 %s' % (os.path.join(config.work_dir, id, 'main.pyc'))
        main_exe = shlex.split(cmd)
    elif language == 'python3':
        cmd = 'python3 %s' % (os.path.join(config.work_dir, id, config.python_exe_name))
        main_exe = shlex.split(cmd)
    else:
        main_exe = [os.path.join(config.work_dir, id, 'main'), ]
    runcfg = {
        'args': main_exe,
        'fd_in': input_data.fileno(),
        'fd_out': temp_out_data.fileno(),
        'timelimit': time_limit,  # in MS
        'memorylimit': mem_limit,  # in KB
    }
    low_level()
    rst = lorun.run(runcfg)
    input_data.close()
    temp_out_data.close()
    logging.debug(rst)
    return rst

