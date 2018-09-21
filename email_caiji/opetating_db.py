#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
import traceback
import sys
reload(sys)
sys.setdefaultencoding('utf8')


# 数据库的操作
def open_db():
    # 开启数据库
    print '开启数据库'
    conn = MySQLdb.connect(host='192.168.1.4', user='root', passwd='666', db='spider', port=3306, charset='gbk')
    cursor = conn.cursor()
    return conn, cursor

def get_companys(cursor):
    # 获取公司信息
    sql = 'select etid,etname from et_info'
    cursor.execute(sql)
    companys = cursor.fetchall()
    return companys

def replace_db(conn, item, table_name):
    """
    向数据库插入一条数据的方法
    :param item: 要写入数据库的数据字典
    :param table_name: 表名
    :return:
    """
    cur = conn.cursor()
    sql1 = "replace into %s(" % table_name
    sql2 = ") values("
    sql3 = ")"
    for key in item.keys():
        sql1 += key + ','
        sql2 += "'" + MySQLdb.escape_string(unicode(item[key])).replace("（", "(").replace("）", ")").strip().encode(
            'gbk', errors='ignore') + "',"
    sql = sql1[:-1] + sql2[:-1] + sql3
    #print sql
    try:
        print '正在存储、、'
        # print sql
        cur.execute(sql)

    except:
        conn.rollback()
        print '插入失败，回滚！'
        traceback.print_exc()


def down_db(conn, cursor):
    # 关闭数据库
    conn.commit()
    cursor.close()
