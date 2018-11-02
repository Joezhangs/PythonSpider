#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:吉祥鸟
# datetime:2018/10/9 13:43
# software: PyCharm

import time
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def open_local_db(db="spider"):
    """
    开启本地数据库
    :param db: 数据库（默认为spider）
    :return: 创建好的数据库连接
    """
    print time.ctime(), '连接本地数据库%s' % db
    conn = MySQLdb.connect(host='192.168.1.4', user='root', passwd='666', db=db, port=3306, charset='gbk')
    return conn

def select_one():
    conn = open_local_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM et_dingding WHERE id=(SELECT MAX(id) FROM et_dingding)"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    return result

def insert_update_one(conn, item, table_name):

    """
    单条数据插入或更新到数据库（注：插入的数据包含表里的关键字）
    :param conn:数据库
    :param item:插入的数据字典（字典类型）
    :param table_name:数据库表名
    :return:无
    """
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
    sql = sql1+sql2[:-1]+sql3[:-1]+sql4[:-1]
    cursor.execute(sql, item_values)
    conn.commit()
    conn.close()

def get_etid(d):
    """
    获取未处理的etid
    :return:
    """
    conn = open_local_db()
    cursor = conn.cursor()
    SQL = "select etid from et_info_status where url_status=1 limit %s" % d
    cursor.execute(SQL)
    result = cursor.fetchall()
    conn.close()
    return result

def optimi():
    res = select_one()
    a = res[0][3]
    print a
    if a < 1000:
        d = 1000 - a
        etids = get_etid(d)
        print etids
    for etid in etids:
        etidz = {}
        print etid[0]
        etidz['etid'] = etid[0]
        etidz["addtime"] = time.time()
        etidz['url_status'] = 2
        etidz["email_status"] = 2
        conn = open_local_db()
        insert_update_one(conn, etidz, "et_info_status")


if __name__ == "__main__":
    optimi()
