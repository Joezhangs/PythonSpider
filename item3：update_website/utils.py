#!/usr/bin/env python
# -*- coding: utf-8 -*-
import torndb
import MySQLdb
from settings import config_dict
import time
import traceback
import logging


def open_line_db(db="lz_datastore"):
    """
    开启本地数据库
    :param db: 数据库（默认为spider）
    :return: 创建好的数据库连接
    """
    print current_time(), '连接线上数据库%s' % db
    conn = MySQLdb.connect(host='rm-2zeuz492sf50a2t27ko.mysql.rds.aliyuncs.com',
                           user='gcdata2012',
                           passwd='gdlz_2017',
                           db=db,
                           port=3306,
                           charset='gbk')
    return conn


def open_local_db(db="spider"):
    """
    开启本地数据库
    :param db: 数据库（默认为spider）
    :return: 创建好的数据库连接
    """
    print current_time(), '连接本地数据库%s' % db
    conn = MySQLdb.connect(host='192.168.1.4', user='root', passwd='666', db=db, port=3306, charset='gbk')
    return conn


def replace_db(res):
    conn = get_local_db()
    para = [[i, int(time.time())] for i in res]
    try:
        conn.executemany("replace into et_info_status(etid,addtime) values(%s,%s)", para)
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

def get_write_db(db='lz_datastore'):
    """
    获取线上数据库连接
    :param db: 连接用的数据库名称，默认lz_datastore
    :return: 创建好的数据库连接
    """
    conn = torndb.Connection(
        host='{}:{}'.format(config_dict['WRITE_DB_MAP_HOST'], config_dict['WRITE_DB_MAP_PORT']),
        database=db,
        user=config_dict['WRITE_DB_USER'],
        password=config_dict['WRITE_DB_PWD'],
    )
    return conn


def current_time():
    """
    获取格式化的当前时间
    :return:获取格式化的当前时间
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def insert_update_many(conn, items, table_name):

    """
    多条数据插入或更新到数据库（注：插入的数据包含表里的关键字）
    :param conn:数据库
    :param items:插入的数据列表字典（列表内包含字典类型）
    :param table_name:数据库表名
    :return:无
    """
    logging.info('%s 开始将数据更新到数据表 ' % current_time())
    cursor = conn.cursor()
    sql1 = "insert into %s" % table_name
    sql2 = "("
    sql3 = ") values("
    sql4 = ")on duplicate key update "
    for key in items[0].keys():  # 拼接sql语句
        sql2 += "%s," % key
        sql3 += "%s,"
        sql4 += "%s=values(%s)," % (key, key)
    sql = sql1 + sql2[:-1] + sql3[:-1] + sql4[:-1]
    item_values = []
    for item in items:
        item_values.append(list(item.values()))
    num = len(item_values)
    print current_time(), '一共需要处理数据%s条' % num
    for i in range(0, num, 1000):
        a = min(num, 1000 + i)
        cursor.executemany(sql, item_values[i:a])
        conn.commit()
        print current_time(), "当前已经处理%s条数据" % a
    conn.close()
    return num


def insert_one(date):
    conn = open_local_db()
    cursor = conn.cursor()
    sql = "insert into et_dingding(type,addtime,total,suc_num) values(%s, {}, %s, %s)".format(time.time())
    cursor.execute(sql, date)
    conn.commit()
    conn.close()
