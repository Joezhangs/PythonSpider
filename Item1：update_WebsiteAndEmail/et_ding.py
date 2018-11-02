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
这个是用于钉钉推送的一个脚本，运行之后可以将相关信息推送到钉钉上，在服务器设置定时任务，可以定时推送信息，就可以监控爬虫的运行情况了
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
    print  '连接本地数据库%s' % db
    conn = MySQLdb.connect(host='192.168.1.4', user='root', passwd='666', db=db, port=3306, charset='gbk')
    return conn



def select_one(time, type):
    conn = open_local_db()
    cursor = conn.cursor()
    sql = "select total,suc_num from et_dingding where type={} and addtime<%s and addtime>%s ".format(type)
    cursor.execute(sql, time)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result

def main():
    now_time = datetime.datetime.now()
    yes_time = now_time + datetime.timedelta(days=-1)
    print yes_time
    # 将python的datetime转换为unix时间戳
    un_time = time.mktime(yes_time.timetuple())
    tim = (time.time(), un_time)
    # 钉钉提醒之email
    results = select_one(tim, 2)
    # print results
    num1 = 0
    a1 = 0
    for result in results:
        num1 += result[0]
        a1 += result[1]
    text = "# 24小时内更新email情况统计\n\n----------\n\n- 总更新数：%s " \
           "\n\n- 更新成功数：%s" \
           "\n\n- 更新失败数：%s" % (num1, a1, num1 - a1)
    url = "http://47.95.214.108:6312/add/"
    data = {
        'text': text,
        'access_token': '1e28405a87104513864b952cbeb5fcbcf6cec68374d053f2ac3eacf690df04ce',
        "title": "数据运营机器人"
    }
    html = requests.post(url, data=data).text
    print html

    # 钉钉提醒之官网url
    results2 = select_one(tim, 1)
    # print results
    num2 = 0
    a2 = 0
    for result2 in results2:
        num2 += result2[0]
        a2 += result2[1]
    text = "# 24小时内更新官网URL情况统计\n\n----------\n\n- 总更新数：%s " \
           "\n\n- 更新成功数：%s" \
           "\n\n- 更新失败数：%s" % (num2, a2, num2 - a2)
    url = "http://47.95.214.108:6312/add/"
    data = {
        'text': text,
        'access_token': '1e28405a87104513864b952cbeb5fcbcf6cec68374d053f2ac3eacf690df04ce',
        "title": "数据运营机器人"
    }
    html = requests.post(url, data=data).text
    print html

main()
