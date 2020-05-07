#!/usr/bin/env python
# coding=utf-8

import os
import threading

def low_level():
    try:
        os.setuid(int(os.popen("id -u %s" % "nobody").read()))
    except:
        pass

# 创建数据库锁，保证一个时间只能一个程序都写数据库
dblock = threading.Lock()
