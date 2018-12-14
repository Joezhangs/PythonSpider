#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:吉祥鸟
# datetime:2018/10/22 14:41
# software: PyCharm
import time
import pymysql
import requests
import random
import warnings

warnings.filterwarnings("ignore")


def open_local_db(db="spider"):
    """
    开启本地数据库
    :param db: 数据库（默认为spider）
    :return: 创建好的数据库连接
    """
    print(now_time(), '连接本地数据库%s' % db)
    conn = pymysql.connect(host='192.168.1.4', user='root', passwd='666', db=db, port=3306, charset='utf8')
    return conn


def open_line_db(db="lz_datastore"):
    """
    开启线上数据库
    :param db: 数据库（默认为spider）
    :return: 创建好的数据库连接
    """
    print(now_time(), '连接线上数据库%s' % db)
    conn = pymysql.connect(host='***',
                           user='***',
                           passwd='***',
                           db=db,
                           port=3306,
                           charset='gbk')
    return conn


def SpCharReplace(char):
    # char=char
    temp = str(char)
    for i in temp:
        if '<' == i:
            char = char.replace('<', '《')
        if '>' == i:
            char = char.replace('>', '》')
        if '\'' == i:
            char = char.replace('\'', '')  # 处理单引号
        if '\\' == i:
            char = char.replace('\\', '')  # 处理反斜杠\
        if '\"' == i:
            char = char.replace('\"', '`')  # 处理双引号"
        if '&' == i:
            char = char.replace('&', '-')  # 处理&号"
        if '|' == i:
            char = char.replace('|', '')  # 处理&号
        if '@' == i:
            char = char.replace('@', '.')  # 处理@号
        if '%' == i:
            char = char.replace('%', "`")  # 处理单引号
        if '*' == i:
            char = char.replace('*', '`')  # 处理反斜杠\
        if '("' == i:
            char = char.replace('\"', '`')  # 处理双引号"
        if ')"' == i:
            char = char.replace(')"', '`')
        if '-' == i:
            char = char.replace('-', '`')  # 处理&号
        if 'ÐÂÎÅ' == i:
            char = char.replace('ÐÂÎÅ', '`')  # 处理ÐÂÎÅ
        # 在后面扩展其他特殊字符
    return char


def select_one(conn):
    """
    查询信息
    :param time:
    :param type:
    :return:
    """
    cursor = conn.cursor()
    sql = "select etid,et_name from et_name_status where status=0 limit 1000"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
        return result
    except:
        print(now_time(), '更新数据失败，回滚')
        conn.rollback()
    conn.close()


def insert_update_one(conn, item, table_name):
    """
    单条数据插入或更新到数据库（注：插入的数据包含表里的关键字）
    :param conn:数据库
    :param item:插入的数据字典（字典类型）
    :param table_name:数据库表名
    :return:无
    """
    print(now_time(), "更新数据表{}.....".format(table_name))
    # print("item:", item)
    if item:
        cursor = conn.cursor()
        sql1 = "insert into %s" % table_name
        sql2 = "("
        sql3 = ") values("
        sql4 = ")on duplicate key update "
        for key in item.keys():  # 拼接sql语句
            sql2 += "%s," % key
            sql3 += "%s,"
            sql4 += "%s=values(%s)," % (key, key)
        try:
            item_values = list(item.values())
            item_values[1] = str(item_values[1])
            # print item_values
            sql = sql1 + sql2[:-1] + sql3[:-1] + sql4[:-1]
            # print(sql)
            cursor.execute(sql, item_values)
            conn.commit()
            print(now_time(), "数据更新成功")
        except:
            print(now_time(), '更新数据失败，回滚')
            conn.rollback()
    else:
        print("无数据")
    conn.close()


def insert_update_many(conn, items, table_name):
    """
    多条数据插入或更新到数据库（注：插入的数据包含表里的关键字）
    :param conn:数据库
    :param items:插入的数据列表字典（列表内包含字典类型）
    :param table_name:数据库表名
    :return:无
    """
    print(now_time(), "更新数据表{}...".format(table_name))
    # print("item:", items)
    if items:
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
        print(now_time(), '一共需要处理数据%s条' % num)

        try:
            for i in range(0, num, 1000):
                a = min(num, 1000 + i)
                cursor.executemany(sql, item_values[i:a])
                conn.commit()
                print(now_time(), "当前已经处理%s条数据" % a)
        except:
            print(now_time(), '更新数据失败，回滚')
            conn.rollback()
    conn.close()


def now_time():
    """
    格式化返回当前时间
    :return:
    """
    now = int(time.time())
    local_time = time.localtime(now)
    format_now = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    return format_now
