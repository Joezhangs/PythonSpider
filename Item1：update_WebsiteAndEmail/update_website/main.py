#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests
import opetating_db
import utils
from process_website import get_website
from gevent import monkey
from gevent.pool import Pool
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf8')
monkey.patch_all()

logging.basicConfig(filename='logger.log', level=logging.INFO)
logging.info("——————————开始更新官网URL————————————")
a = 0
et_info_urls = []
et_statuss = []
def spider(et_date):
    # print et_date
    if et_date != []:
        et_info_url = get_website(et_date[0])
        et_info_url['etupdatetime'] = time.time()
        et_info_urls.append(et_info_url)
        et_status = {}
        if et_info_url['etwebsite']:
            print utils.current_time(), '正在更新状态表数据status=3......'
            et_status['etid'] = et_info_url['etid']
            et_status["addtime"] = time.time()
            et_status['url_status'] = 3
            global a
            a += 1
            # print et_status
            et_statuss.append(et_status)
        else:
            print utils.current_time(), '正在更新状态表数据status=2......'
            et_status['etid'] = et_info_url['etid']
            et_status["addtime"] = time.time()
            et_status['url_status'] = 2
            # print et_status
            et_statuss.append(et_status)
    # print et_info_url



def main():
    et_dingding = []
    etids = opetating_db.get_etid()
    et_dates = opetating_db.get_companys(etids)
    pool = Pool(15)
    pool.map(spider, et_dates)
    pool.join()
    conn = utils.open_line_db()
    num = utils.insert_update_many(conn, et_info_urls, 'et_info')
    con = utils.open_local_db()
    utils.insert_update_many(con, et_statuss, 'et_info_status')
    logging.info("%s 添加钉钉数据" % utils.current_time())
    type = 1
    et_dingding.append(type)
    et_dingding.append(num)
    et_dingding.append(a)
    utils.insert_one(et_dingding)
    logging.info("—————————结束更新官网URL——————————")
    # text = "# 本次更新官网url情况统计\n\n----------\n\n- 本次总更新数：%s " \
    #     "\n\n- 更新成功数：%s" \
    #     "\n\n- 更新失败数：%s" % (num, a, num-a)
    # url = "http://47.95.214.108:6312/add/"
    # data = {
    #     'text': text,
    #     'access_token': '75c1562dfa4297dbb5e11452983db916d9685544679e99ab3ccc898f52c69285',
    # }
    # html = requests.post(url, data=data).text
    # print html
    # et_info_urls.append(et_info_url)
    # partial_work = partial(get_website, conn)
    # pool = Pool(15)
    # pool.map(partial_work, et_dates)
    # pool.join()
    # conn.close()
    # print ("关闭数据库")


if __name__ == "__main__":
    main()
    print "结束爬虫"
