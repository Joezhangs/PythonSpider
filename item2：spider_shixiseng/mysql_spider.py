
# ._*_.coding:utf-8_*_
import MySQLdb
import traceback
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def replace_into_mysql(conn, item, table_name):

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
        cur.execute(sql)
    except:
        conn.rollback()
        print '插入失败，回滚！'
        traceback.print_exc()

