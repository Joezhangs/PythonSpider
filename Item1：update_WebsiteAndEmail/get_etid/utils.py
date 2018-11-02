#!/usr/bin/env python
# -*- coding: utf-8 -*-
import torndb
from settings import config_dict
import time
import traceback

def replace_db(res):
    conn = get_local_db()
    para = [[i, int(time.time())] for i in res]
    # print para
    try:
        conn.executemany("insert into et_info_status(etid,addtime) values(%s,%s)on duplicate key update etid=values(etid), addtime=values(addtime)", para)
    except:
        traceback.print_exc()
    return conn

def get_local_db(db='spider'):
    """
    获取线下数据库连接
    :param db:连接用的数据库名称，默认caiji_email
    :return:创建好的数据库连接
    """
    conn = torndb.Connection(
        host='{}:{}'.format(config_dict['LOCAL_DB_HOST'], config_dict['LOCAL_DB_PORT']),
        database=db,
        user=config_dict['LOCAL_DB_USER'],
        password=config_dict['LOCAL_DB_PWD'],
    )
    return conn

def get_read_db(db='lz_datastore'):
    """
    获取从数据库连接
    :param db: 连接用的数据库名称，默认lz_datastore
    :return: 创建好的数据库连接
    """
    conn = torndb.Connection(
        host='{}:{}'.format(config_dict['READ_DB_HOST'], config_dict['READ_DB_PORT']),
        database=db,
        user=config_dict['READ_DB_USER'],
        password=config_dict['READ_DB_PWD'],
    )
    return conn

def current_time():
    """
    获取格式化的当前时间
    :return:获取格式化的当前时间
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))