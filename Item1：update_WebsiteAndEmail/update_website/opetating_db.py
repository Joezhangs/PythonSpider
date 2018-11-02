#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
import traceback
import logging
import utils
import sys
reload(sys)
sys.setdefaultencoding('utf8')


# 数据库的操作

def get_etid():
    """
    获取未处理的etid
    :return:
    """
    logging.info('%s 本地表中读取所有未处理的etid...' % utils.current_time())
    conn = utils.get_local_db()
    result = conn.query("select etid from et_info_status where url_status=1 limit 200")
    conn.close()
    return result


def get_companys(etids):
    # 获取公司信息
    companys = []
    conn = utils.get_read_db()
    print utils.current_time(), '从线上读取部分的etid的信息 '
    logging.info('%s 从线上读取部分的etid的信息 ' % utils.current_time())
    for etid in etids:
        # print etid
        sql = 'select etid,etname,etwebsite,etfullname from et_info where etid={}'.format(etid['etid'])
        result = conn.query(sql)
        companys.append(result)
    return companys
    conn.close()


def update_db(conn, item, table_name):
    """
    向数据库更新一条数据的方法
    :param item: 要写入数据库的数据字典
    :param table_name: 表名
    :return:
    """

    sql1 = "update %s " % table_name
    sql2 = "set "
    for key in item.keys():
        date = item[key]
        if key == 'etid':
            sql3 = ' where %s = "%s"' % (key, date)
        else:
            sql2 += '%s = "%s",' % (key, date)
    sql = sql1 + sql2[:-1] + sql3
    print sql
    # print '正在存储、、'
        # print sql
    conn.execute(sql)
    conn.close()


def update_status_db(et_info_url):
    if et_info_url['etwebsite']:
        print utils.current_time(), '正在更新状态表数据status=3......'
        conn = utils.get_local_db()
        et_status = {}
        et_status['etid'] = et_info_url['etid']
        et_status['url_status'] = 3
        update_db(conn,et_status,'et_info_status')
    else:
        print utils.current_time(), '正在更新状态表数据status=2......'
        conn = utils.get_local_db()
        et_status = {}
        et_status['etid'] = et_info_url['etid']
        et_status['url_status'] = 2
        update_db(conn, et_status, 'et_info_status')



