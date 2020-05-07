#!/usr/bin/env python
# coding=utf-8
import logging
import time
import pymysql
from judger import config


def run_sql(sql):
    '''执行sql语句,并返回结果'''
    con = None
    while True:
        try:
            con = pymysql.connect(config.db_host, config.db_user, config.db_password,
                                  config.db_name, charset=config.db_charset)
            break
        except:
            logging.error('Cannot connect to database,trying again')
            time.sleep(1)
    cur = con.cursor()
    try:
        if type(sql) == str:
            cur.execute(sql)
        elif type(sql) == list:
            for i in sql:
                cur.execute(i)
    except pymysql.OperationalError as e:
        logging.error(e)
        cur.close()
        con.close()
        return False
    con.commit()
    data = cur.fetchall()
    cur.close()
    con.close()
    return data


def run_sql_without_return(sql):
    '''执行sql语句,不返回结果'''
    con = None
    while True:
        try:
            con = pymysql.connect(config.db_host, config.db_user, config.db_password,
                                  config.db_name, charset=config.db_charset)
            break
        except:
            logging.error('Cannot connect to database,trying again')
            time.sleep(1)
    cur = con.cursor()
    try:
        if type(sql) == str:
            cur.execute(sql)
        elif type(sql) == list:
            for i in sql:
                cur.execute(i)
    except pymysql.OperationalError as e:
        logging.error(e)
        cur.close()
        con.close()
        return False
    con.commit()
    cur.close()
    con.close()
    return True
