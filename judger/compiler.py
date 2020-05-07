#!/usr/bin/env python
# coding=utf-8
import os

from judger import config
import subprocess

from judger.deal_data import update_compile_info
from judger.protect import low_level, dblock


def compiler(id, language):
    low_level()
    '''将程序编译成可执行文件'''
    language = language.lower()
    dir_work = os.path.join(config.work_dir, id)# 路径拼接
    build_cmd = {
        "gcc": "gcc main.c -o main",
        "g++": "g++ main.cpp -o main",
        "java": "javac Main.java",
        "python2": 'python2 -m py_compile main.py',
        "python3": 'python3 -m py_compile main.py',
    }
    if language not in build_cmd.keys():
        return False
    p = subprocess.Popen(
        build_cmd[language],
        shell=True,
        cwd=dir_work,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    out, err = p.communicate()  # 获取编译信息
    err_txt_path = os.path.join(config.work_dir, id, 'error.txt')
    str_out = str(out, encoding='utf-8')
    str_err = str(err, encoding='utf-8')
    f = open(err_txt_path, 'w')
    f.write(str_err)
    f.write(str_out)
    f.close()
    if p.returncode == 0:  # 返回值为0,编译成功
        return True
    dblock.acquire()
    update_compile_info(id, str_err + str_out)  # 编译失败,更新题目的编译错误信息
    dblock.release()
    return False
