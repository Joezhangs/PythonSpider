#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
import traceback
import utils
import sys
import logging
reload(sys)
sys.setdefaultencoding('utf8')


# 数据库的操作
def open_db():
    # 开启数据库
    print '开启数据库'
    conn = MySQLdb.connect(host='192.168.1.4', user='root', passwd='666', db='spider', port=3306, charset='gbk')
    cursor = conn.cursor()
    return conn, cursor

# def get_companys(cursor):
#     # 获取公司信息
#     sql = 'select etid,etname from et_info'
#     cursor.execute(sql)
#     companys = cursor.fetchall()
#     return companys

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

def get_etid():
    """
    获取未处理的etid
    :return:
    """
    print utils.current_time(), '本地表中读取部分未处理的etid...'
    logging.info('%s 本地表中读取所有未处理的etid...' % utils.current_time())
    conn = utils.get_local_db()
    result = conn.query("select etid from et_info_status where email_status=1 limit 200")
    conn.close()
    return result


def get_companys(etids):
    # 获取公司信息
    companys = []
    conn = utils.get_read_db()
    print utils.current_time(), '从线上读取部分的etid公司的信息 '
    logging.info('%s 从线上读取部分的etid的信息 ' % utils.current_time())
    for etid in etids:
        # print etid
        sql = 'select etid,etname from et_info where etid={}'.format(etid['etid'])
        result = conn.query(sql)
        companys.append(result)
    return companys
    conn.close()

def down_db(conn, cursor):
    # 关闭数据库
    conn.commit()
    cursor.close()
