#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:吉祥鸟
# datetime:2018/10/22 14:41
# software: PyCharm
import time
import MySQLdb
import requests
import random
import sys
import warnings
warnings.filterwarnings("ignore")
reload(sys)
sys.setdefaultencoding('utf8')
"""
个人常用工具库（此库不是所有的代码都会使用）

请求模块：get_url_html()
连接本地库（默认spider）：open_local_db()
连接线上库（默认lz_datastore）：open_line_db()
数据库查询信息：select_one()（需修改）
单条信息插入或更新：insert_update_one()
多条信息插入或更新insert_update_many()
单条信息更新：update_one()
获取格式化时间：now_time()

"""


def get_url_html(url,ip=False):
    """
    get请求url的函数
    :param url:
    :ip：是否使用代理ip,默认不使用
    :return: 未解析的html
    """
    z = 0
    user_agents = [
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
         ]

    us = random.choice(user_agents)
    headers = {
        'User-Agent': us
    }
    # 设置代理
    proxy = "****"
    proxies = {
        "http": "http://" + proxy,
        "https": "https://" + proxy,
    }
    print ("本次请求的URL为：%s"% url)
    try:
        for i in range(1, 3):
            print now_time(), "第%s次请求" % i,
            try:
                if ip==True:
                    html = requests.get(url, headers=headers, proxies=proxies, timeout=4)
                    time.sleep(1)
                else:
                    html = requests.get(url, headers=headers, timeout=4)
                    time.sleep(1)
                if html.status_code == 200:
                    if "快捷登录" not in html.text or "密码登录" not in html.text:
                        z = 1
                        break
                    else:
                        print "页面数据异常,再次尝试请求......"
                else:
                    print "请求出错,再次尝试请求......"
            except:
                print "请求出错,再次尝试请求......"
        if z == 1:
            print '本次请求成功'
            return html.content
        else:
            print now_time(), "请求超过最大次数，跳过"
            time.sleep(0.5)
            return
        # print html
    except:
        print now_time(), '%s请求失败'%url
        return


def open_local_db(db="spider"):
    """
    开启本地数据库
    :param db: 数据库（默认为spider）
    :return: 创建好的数据库连接
    """
    print now_time(), '连接本地数据库%s' % db
    conn = MySQLdb.connect(host='192.168.1.4', user='root', passwd='666', db=db, port=3306, charset='gbk')
    return conn


def open_line_db(db="lz_datastore"):
    """
    开启线上数据库
    :param db: 数据库（默认为spider）
    :return: 创建好的数据库连接
    """
    print now_time(), '连接线上数据库%s' % db
    conn = MySQLdb.connect(host='r***',
                           user='***',
                           passwd='***',
                           db=db,
                           port=3306,
                           charset='gbk')
    return conn


def insert_update_one(conn, item, table_name):

    """
    单条数据插入或更新到数据库（注：插入的数据包含表里的关键字）
    :param conn:数据库
    :param item:插入的数据字典（字典类型）
    :param table_name:数据库表名
    :return:无
    """
    if item:
        print now_time(), "更新数据....."
        cursor = conn.cursor()
        sql1 = "insert into %s" % table_name
        sql2 = "("
        sql3 = ") values("
        sql4 = ")on duplicate key update "
        for key in item.keys():  # 拼接sql语句
            sql2 += "%s," % key
            sql3 += "%s,"
            sql4 += "%s=values(%s)," % (key, key)
        item_values = list(item.values())
        item_values[1] = str(item_values[1]).encode("gbk")
        # print item_values
        sql = sql1+sql2[:-1]+sql3[:-1]+sql4[:-1]
        # print sql
        cursor.execute(sql, item_values)
        conn.commit()
        print now_time(), "数据更新成功"


def insert_update_many(conn, items, table_name):

    """
    多条数据插入或更新到数据库（注：插入的数据包含表里的关键字）
    :param conn:数据库
    :param items:插入的数据列表字典（列表内包含字典类型）
    :param table_name:数据库表名
    :return:无
    """

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
        print now_time(), '一共需要处理数据%s条' % num
        print sql
        try:
            for i in range(0, num, 1000):
                a = min(num, 1000 + i)
                cursor.executemany(sql, item_values[i:a])
                conn.commit()
                print now_time(), "当前已经处理%s条数据" % a
        except:
            print now_time(), '更新数据失败，回滚'
            conn.rollback()
        conn.close()
    else:
        print items



def update_one(db, item, table_name):
    """
    向数据库更新一条数据的方法
    :param item: 要写入数据库的数据字典
    :param table_name: 表名
    :return:
    """
    cursor = db.cursor()
    sql1 = "update %s " % table_name
    sql2 = "set "
    for key in item.keys():
        date = item[key]
        if key == 'etid':
            sql3 = ' where %s = "%s"' % (key, date)
        else:
            sql2 += '%s = "%s",' % (key, date)
    sql = sql1 + sql2[:-1] + sql3
    try:
        cursor.execute(sql)
        cursor.commit()
    except:
        print now_time(), '更新数据失败，回滚'
        db.rollback()
    db.close()


def now_time():
    """
    格式化返回当前时间
    :return:
    """
    now = int(time.time())
    local_time = time.localtime(now)
    format_now = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    return format_now


def select_one(conn):
    """
    查询信息
    :param time:
    :param type:
    :return:
    """
    cursor = conn.cursor()
    sql = "select etid,et_name from et_name_status where status=0 limit 100"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
        return result
    except:
        print time.time(), '获取数据失败，回滚'
        conn.rollback()
    conn.close()

def select_ones(conn):
    """
    查询信息
    :param time:
    :param type:
    :return:
    """
    cursor = conn.cursor()
    a = 101260000
    b = 101270000
    while True:
        sql1 = "select etid,etname from et_info "
        sql2 = "where etid>%s and etid<%s" % (a, b)
        sql = sql1+sql2
        print sql
        try:
            a = b
            b = a + 10000
            cursor.execute(sql)
            result = cursor.fetchall()
            conn.commit()
            # print "result:",result
            if result:
                yield result
            else:
                if a > 120000000:
                    break
        except:
            print time.ctime(), '获取数据失败，回滚'
            conn.rollback()
    conn.close()


def insert_ignore_many(conn, items, table_name):
    """
    多条数据插入(若存在，则忽略)到数据库（注：插入的数据包含表里的关键字）
    :param conn:数据库
    :param items:插入的数据列表字典（列表内包含字典类型）
    :param table_name:数据库表名
    :return:无
    """

    if items:
        cursor = conn.cursor()
        sql1 = "insert ignore into %s" % table_name
        sql2 = "("
        sql3 = ") values("
        sql4 = ") "
        for key in items[0].keys():  # 拼接sql语句
            sql2 += "%s," % key
            sql3 += "%s,"
        sql = sql1 + sql2[:-1] + sql3[:-1] + sql4[:-1]
        item_values = []
        for item in items:
            item_values.append(list(item.values()))
        num = len(item_values)
        print now_time(), '一共需要处理数据%s条' % num
        print sql
        try:
            for i in range(0, num, 1000):
                a = min(num, 1000 + i)
                cursor.executemany(sql, item_values[i:a])
                conn.commit()
                print now_time(), "当前已经处理%s条数据" % a
        except:
            print now_time(), '更新数据失败，回滚'
            conn.rollback()
        conn.close()
    else:
        print items


def insert_ignore_one(db, item, table_name):
    """
    向数据库插入忽略一条数据的方法
    :param item: 要写入数据库的数据字典
    :param table_name: 表名
    :return:
    """
    if item:
        cursor = db.cursor()
        sql1 = "insert ignore into %s" % table_name
        sql2 = "("
        sql3 = ") values("
        sql4 = ") "
        for key in item.keys():  # 拼接sql语句
            sql2 += "%s," % key
            sql3 += "'%s'," % item[key]
        sql = sql1 + sql2[:-1] + sql3[:-1] + sql4[:-1]
        print sql
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print now_time(), '更新数据失败，回滚'
        db.rollback()
