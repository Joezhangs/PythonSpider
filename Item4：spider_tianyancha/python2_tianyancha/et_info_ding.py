#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
import datetime
import time
import requests
import sys

reload(sys)
sys.setdefaultencoding('utf8')
"""
钉钉信息提醒
"""


# def current_time():
#     """
#     获取格式化的当前时间
#     :return:获取格式化的当前时间
#     """
#     return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def open_local_db(db="spider"):
    """
    开启本地数据库
    :param db: 数据库（默认为spider）
    :return: 创建好的数据库连接
    """
    print('连接本地数据库{}'.format(db))
    conn = MySQLdb.connect(host='192.168.1.4', user='root', passwd='666', db=db, port=3306, charset='gbk')
    return conn


def select_one(time, type):
    conn = open_local_db()
    cursor = conn.cursor()
    sql = "select etid from et_name_status where status={} and update_time<%s and update_time>%s ".format(type)
    cursor.execute(sql, time)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result


def main():
    now_time = datetime.datetime.now()
    yes_time = now_time + datetime.timedelta(days=-1)
    print(yes_time)
    # 将python的datetime转换为unix时间戳
    un_time = time.mktime(yes_time.timetuple())
    tim = (time.time(), un_time)
    # 查询
    results = select_one(tim, 1)
    print(len(results))
    num1 = len(results)
    text = "# 24小时内爬取企业信息情况统计\n\n----------\n\n- 本次更新数：%s " % num1
    url = "http://47.95.214.108:6312/add/"
    data = {
        'text': text,
        'access_token': '***',   # 填写自己的机器人信息
    }
    html = requests.post(url, data=data).text
    print(html)


main()
