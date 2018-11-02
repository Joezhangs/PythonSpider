#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import requests
reload(sys)
sys.setdefaultencoding('utf8')
from optimization import optimi
import utils
import time
from odps import ODPS


logging.basicConfig(filename='logger.log', level=logging.INFO)
logging.info("——————————开始获取etid——————————")
o = ODPS('LTAIzEuNzcL6qJJ8', 'eUAgj9ijhWCvOQ3w5Uv3FkwhNxvPF2', 'database_test', 'http://service.odps.aliyun.com/api')

def get_int_day():
    """
    获取当前日期的00:00:00的整型值
    :return:
    """
    x1 = time.strftime("%Y-%m-%d 00:00:00", time.localtime(time.time()))
    x2 = time.mktime(time.strptime(x1, "%Y-%m-%d %H:%M:%S"))
    return int(x2)


today_int = get_int_day()
yesterday_int = today_int - 24 * 60 * 60
before_yesterday = yesterday_int - 24 * 60 * 60
pt = time.strftime("%Y%m%d", time.localtime(yesterday_int))


# A类企业
def get_etid_set_from_collect():
    """
    获取A类企业的etid，写入到数据库
    :return:
    """
    print utils.current_time(), '获取A类企业'
    logging.info('1. 获取A类企业 ')
    conn = utils.get_read_db()
    xx = conn.query("select etid from et_info_collect where ettype=1")
    res = set([])
    for i in xx:
        res.add(i['etid'])
    conn.close()
    print utils.current_time(), 'A类企业获取完成，准备写入数据库'
    conn = utils.replace_db(res)
    print utils.current_time(), 'A类企业写入完成'
    conn.close()
    res = len(res)
    return res


# A轮及A轮后融资企业
def get_etid_set_from_et_financing():
    """
    获取A轮及A轮后融资企业的etid，写入到数据库
    :return:
    """
    print utils.current_time(), '获取A轮及A轮后融资企业'
    logging.info('2. 获取A轮及A轮后融资企业 ')
    conn = utils.get_read_db()
    xx = conn.query("select etid from et_financing where rounds>9")
    res = set([])
    for i in xx:
        res.add(i['etid'])
    conn.close()
    print utils.current_time(), 'A轮及A轮后融资企业获取完成，准备写入数据库'
    conn = utils.replace_db(res)
    print utils.current_time(), 'A轮及A轮后融资企业写入完成'
    conn.close()
    res = len(res)
    return res


# 有猎头经历
def get_etid_set_from_et_info_collect_lt():
    """
    获取有猎头经历的etid，写入到数据库
    :return:
    """
    print utils.current_time(), '获取有猎头经历的企业'
    logging.info('3. 获取有猎头经历的企业 ')
    conn = utils.get_read_db()
    xx = conn.query("select etid from et_info_collect where lt_company=1")
    res = set([])
    for i in xx:
        res.add(i['etid'])
    conn.close()
    print utils.current_time(), '有猎头经历的企业获取完成，准备写入数据库'
    conn = utils.replace_db(res)
    print utils.current_time(), '有猎头经历的企业写入完成'
    conn.close()
    res = len(res)
    return res


# 猎聘有职位的企业
def get_etid_set_from_et_jobs_liepin():
    """
    获取在猎聘有职位的企业的etid，写入到数据库
    :return:
    """
    print utils.current_time(), '获取在猎聘有职位的企业'
    logging.info('4. 获取在猎聘有职位的企业 ')
    result = o.execute_sql("select etid from et_jobs where pt='{}' and job_outsite like '%liepin%'".format(pt))
    res = set()
    with result.open_reader() as reader:
        for record in reader:
            res.add(record['etid'])
    print utils.current_time(), '在猎聘有职位的企业获取完成，准备写入数据库'
    conn = utils.replace_db(res)
    print utils.current_time(), '在猎聘有职位的企业写入完成'
    conn.close()
    res = len(res)
    return res


# 拉勾plus
def get_etid_set_from_et_jobs_lagou():
    """
    获取拉勾plus企业的etid，写入到数据库
    :return:
    """
    print utils.current_time(), '获取拉勾plus企业'
    logging.info('5. 获取拉勾plus企业 ')
    result = o.execute_sql(
        "select count(etid) as job_cnt,etid from et_jobs where pt='{}' and job_outsite like '%lagou%' GROUP BY etid".format(
            pt))
    res = set()  # 创建一个无序的不重复的元素集
    with result.open_reader() as reader:
        for record in reader:
            if int(record['job_cnt']) > 5:
                res.add(record['etid'])
    print utils.current_time(), '拉勾plus', len(res)
    print utils.current_time(), '拉勾plus企业获取完成，准备写入数据库'
    conn = utils.replace_db(res)
    print utils.current_time(), '拉勾plus企业写入完成'
    conn.close()
    res = len(res)
    return res


# 拜访记录晚于 1419120000
def get_etid_set_from_et_info_extend():
    """
    获取2015年后有拜访记录的企业的etid，写入到数据库
    :param kinds: 企业种类
    :param caiji_date:采集批次
    :return:
    """
    print utils.current_time(), '获取2015年后有拜访记录的企业'
    logging.info('6. 获取2015年后有拜访记录的企业 ' )
    conn = utils.get_read_db()
    xx = conn.query("select etid from et_info_extend where exVisitTime>1419120000")
    res = set()
    for i in xx:
        res.add(i['etid'])
    conn.close()
    print utils.current_time(), '2015年后有拜访记录的企业获取完成，准备写入数据库'
    conn = utils.replace_db(res)
    print utils.current_time(), '2015年后有拜访记录的企业写入完成'
    conn.close()
    res = len(res)
    return res


# 群好友
def get_etid_set_from_sys_group():
    """
    获取有群好友的企业的etid，写入到数据库
    :return:
    """
    print utils.current_time(), '正在获取有群好友的企业'
    logging.info('7. 正在获取有群好友的企业 ')
    conn = utils.get_read_db(db='lz_crm')
    xx = conn.query("select etid from sys_pub_chatgroup_account where etid!=0")
    res = set()
    for i in xx:
        res.add(i['etid'])
    conn.close()
    print utils.current_time(), '有群好友的企业获取完成，准备写入数据库'
    conn = utils.replace_db(res)
    print utils.current_time(), '有群好友的企业写入完成'
    conn.close()
    res = len(res)
    return res


# 获取联系人中存在微信号的企业etid集合
def get_etid_set_with_weixin_num():
    """
    获取联系人中存在微信号的企业的etid，写入到数据库
    :return:
    """
    print utils.current_time(), '正在获取联系人中存在微信号的企业'
    logging.info('8. 正在获取联系人中存在微信号的企业 ')
    conn = utils.get_read_db(db='lz_datastore')
    xx = conn.query("select etid from et_contact where weixin!=''")
    res = set()
    for i in xx:
        res.add(i['etid'])
    conn.close()
    print utils.current_time(), '联系人中存在微信号的企业获取完成，准备写入数据库'
    conn = utils.replace_db(res)
    print utils.current_time(), '联系人中存在微信号的企业写入完成'
    conn.close()
    res = len(res)
    return res


# 获取BD名下的企业etid集合
def get_etid_set_by_bdname():
    """
    获取联系人中存在微信号的企业的etid，写入到数据库
    :return:
    """
    bdid_list = [200000248, 200000678]  # [赵露露,洪娟]
    print utils.current_time(), '正在获取BD名下的企业'
    logging.info('9. 正在获取BD名下的企业 ')
    conn = utils.get_read_db(db='lz_crm')
    res = set()
    for bdid in bdid_list:
        xx = conn.query("select etid from erpo_company_adviser where createuid={}".format(bdid))
        for i in xx:
            res.add(i['etid'])
    conn.close()
    print utils.current_time(), 'BD名下的企业获取完成，准备写入数据库'
    conn = utils.replace_db(res)
    print utils.current_time(), 'BD名下的企业写入完成'
    conn.close()
    res = len(res)
    return res

def get_36kr_etid():
    logging.info('10. 正在获取36hr的企业 ')
    print utils.current_time(), '建立数据库连接...'
    conn = utils.get_read_db(db='contact_datastore')
    print utils.current_time(), '查询需要采集的etid...'
    res = conn.query("select etid from dt_daily_36kr")
    conn.close()
    print utils.current_time(), '查询完成！'
    insert_list = []
    addtime = int(time.time())
    for x in res:
        insert_list.append([x['etid'], addtime])
    print utils.current_time(), '准备写入数据库...'
    conn = utils.get_local_db()
    total = len(insert_list)
    print utils.current_time(), '共需写入', total, '条！'
    for i in range(0, total, 1000):
        start = i
        end = min(start + 1000, total)
        conn.executemany("insert into et_info_status(etid,addtime) values(%s,%s)on duplicate key update etid=values(etid), addtime=values(addtime)",
                         insert_list[start:end])
        print utils.current_time(), '当前写入 {}/{}！'.format(end, total)
    conn.close()
    print '写入完成！'
    return total

def get_hr_etid():
    logging.info('11. 正在获取hr的企业 ')
    print utils.current_time(), '建立odps链接..'
    o = ODPS('LTAIzEuNzcL6qJJ8', 'eUAgj9ijhWCvOQ3w5Uv3FkwhNxvPF2', 'database_test',
             'http://service.odps.aliyun.com/api')
    print utils.current_time(), '进行查询...'
    pt = time.strftime('%Y%m%d', time.localtime(int(time.time() - 86400)))
    res = o.execute_sql(
        "select distinct etid from et_jobs where pt='{}' and ishrjob!='' and ishrjob!='000000'".format(pt))
    print utils.current_time(), '处理查询结果...'
    etid_set = set()
    conn = utils.get_local_db()
    addtime = int(time.time())
    cnt = 0
    with res.open_reader() as reader:
        print utils.current_time(), '共需处理{}条!'.format(reader.count)
        for record in reader:
            etid_set.add((record['etid'],))
            if len(etid_set) >= 1000:
                conn.executemany("insert into et_info_status(etid,addtime) values(%s,{})on duplicate key update etid=values(etid), addtime=values(addtime)".format(addtime),
                                 list(etid_set))
                cnt += 1000
                print utils.current_time(), '当前已写入{}条!'.format(cnt)
                etid_set.clear()
    if len(etid_set) > 0:
        conn.executemany("insert into et_info_status(etid,addtime) values(%s,{})on duplicate key update etid=values(etid), addtime=values(addtime)".format(addtime),
                         list(etid_set))
        cnt += len(etid_set)
        print utils.current_time(), '当前已写入{}条!'.format(cnt)
    conn.close()
    return reader.count

def get_last_etid():
    logging.info('12. 正在获取其他的企业 ')
    print utils.current_time(), '建立odps链接..'
    o = ODPS('LTAIzEuNzcL6qJJ8', 'eUAgj9ijhWCvOQ3w5Uv3FkwhNxvPF2', 'database_test',
             'http://service.odps.aliyun.com/api')
    print utils.current_time(), '进行查询...'
    pt = time.strftime('%Y%m%d', time.localtime(int(time.time() - 86400)))
    res = o.execute_sql("select distinct etid from et_jobs where pt='{}' and job_updatetime >= 1520611200".format(pt))
    print utils.current_time(), '处理查询结果...'
    etid_set = set()
    conn = utils.get_local_db()
    addtime = int(time.time())
    cnt = 0
    with res.open_reader() as reader:
        print utils.current_time(), '共需处理{}条!'.format(reader.count)
        for record in reader:
            etid_set.add((record['etid'],))
            if len(etid_set) >= 1000:
                conn.executemany("insert into et_info_status(etid,addtime) values(%s,{})on duplicate key update etid=values(etid), addtime=values(addtime)".format(addtime),
                                 list(etid_set))
                cnt += 1000
                print utils.current_time(), '当前已写入{}条!'.format(cnt)
                etid_set.clear()
    if len(etid_set) > 0:
        conn.executemany("insert into et_info_status(etid,addtime) values(%s,{})on duplicate key update etid=values(etid), addtime=values(addtime)".format(addtime),
                         list(etid_set))
        cnt += len(etid_set)
        print utils.current_time(), '当前已写入{}条!'.format(cnt)
    conn.close()
    return reader.count

def get_lt_etid():
    logging.info('12. 正在获取其他的企业 ')
    print utils.current_time(), '建立odps链接..'
    o = ODPS('LTAIzEuNzcL6qJJ8', 'eUAgj9ijhWCvOQ3w5Uv3FkwhNxvPF2', 'database_test',
             'http://service.odps.aliyun.com/api')
    print utils.current_time(), '进行查询...'
    pt = time.strftime('%Y%m%d', time.localtime(int(time.time() - 86400)))
    res = o.execute_sql("select distinct etid from et_jobs where pt='{}' and isheadhunter=1".format(pt))
    print utils.current_time(), '处理查询结果...'
    etid_set = set()
    conn = utils.get_local_db()
    addtime = int(time.time())
    cnt = 0
    with res.open_reader() as reader:
        print utils.current_time(), '共需处理{}条!'.format(reader.count)
        for record in reader:
            etid_set.add((record['etid'],))
            if len(etid_set) >= 1000:
                conn.executemany("insert into et_info_status(etid,addtime) values(%s,{})on duplicate key update etid=values(etid), addtime=values(addtime)".format(addtime),
                                 list(etid_set))
                cnt += 1000
                print utils.current_time(), '当前已写入{}条!'.format(cnt)
                etid_set.clear()
    if len(etid_set) > 0:
        conn.executemany("insert into et_info_status(etid,addtime) values(%s,{})on duplicate key update etid=values(etid), addtime=values(addtime)".format(addtime),
                         list(etid_set))
        cnt += len(etid_set)
        print utils.current_time(), '当前已写入{}条!'.format(cnt)
    conn.close()
    return reader.count

def gen_etid():
    """
    生成需要采集的etid
    :return:
    """
    a = get_etid_set_from_collect()  # 获取A类企业etid
    A = get_etid_set_from_et_financing()  # 获取A轮及A轮后融资企业
    lietou = get_etid_set_from_et_info_collect_lt()  # 获取有猎头经历的企业
    aft2015 = get_etid_set_from_et_info_extend()  # 获取2015年后有拜访记录的企业
    lagou = get_etid_set_from_et_jobs_lagou()  # 获取拉勾plus企业
    zhiwei = get_etid_set_from_et_jobs_liepin()  # 获取在猎聘有职位的企业
    qun = get_etid_set_from_sys_group()  # 获取有群好友的企业
    BD = get_etid_set_by_bdname()   # 获取BD名下的企业
    wei = get_etid_set_with_weixin_num()  # 联系人中存在微信号的企业的etid
    hr36 = get_36kr_etid()  # 获取36kr的企业
    hr = get_hr_etid()  # 获取hr的企业
    last = get_last_etid()
    lt = get_lt_etid()

    text = "# 本次etid获取情况统计\n\n----------\n\n- 获取A类企业数：%s " \
           "\n\n- 获取A轮及A轮后融资企业数：%s" \
           "\n\n- 获取有猎头经历的企业数：%s" \
           "\n\n- 获取2015年后有拜访记录的企业：%s" \
           "\n\n- 获取拉勾plus企业数：%s" \
           "\n\n- 获取在猎聘有职位的企业数：%s" \
           "\n\n- 获取有群好友的企业数：%s" \
           "\n\n- 获取BD名下的企业数：%s" \
           "\n\n- 获取联系人中存在微信号的企业数：%s" \
           "\n\n- 获取36kr的企业数：%s" \
           "\n\n- 获取hr的企业数：%s" \
           "\n\n- 获取其他企业数：%s" % (a, A, lietou, aft2015, lagou, zhiwei, qun, BD, wei, hr36, hr, last+lt)

    url = "http://47.95.214.108:6312/add/"
    data = {
        'text': text,
        'access_token': '1e28405a87104513864b952cbeb5fcbcf6cec68374d053f2ac3eacf690df04ce',
        "title": "数据运营机器人"
    }
    html = requests.post(url, data=data).text
    print html

if __name__ == '__main__':
    gen_etid()
    optimi()
    logging.info("——————————结束获取etid——————————")
