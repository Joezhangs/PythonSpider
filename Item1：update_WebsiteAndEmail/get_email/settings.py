#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

config_dict = {
    'LOCAL_DB_HOST': '192.168.1.4',
    'LOCAL_DB_PORT': 3306,
    'LOCAL_DB_USER': 'root',
    'LOCAL_DB_PWD': '666',
    # 从（只读）数据库内网host
    'READ_DB_HOST': 'rm-2zeuz492sf50a2t27ko.mysql.rds.aliyuncs.com',
    # 从（只读）数据库内网端口
    'READ_DB_PORT': 3306,
    # 从（只读）数据库用户名
    'READ_DB_USER': 'gcdata2012',
    # 从（只读）数据库密码
    'READ_DB_PWD': 'gdlz_2017',
    # 线上（读写）数据库内网host
    'WRITE_DB_MAP_HOST': 'rm-2zeuz492sf50a2t27ko.mysql.rds.aliyuncs.com',
    # 线上（读写）数据库内网端口
    'WRITE_DB_MAP_PORT': 3306,
    # 线上（读写）数据库用户名
    'WRITE_DB_USER': 'gcdata2012',
    # 线上（读写）数据库密码
    'WRITE_DB_PWD': 'gdlz_2017',
    # 站点别称
    'CAIJI_SITE':'email',
    # 最大允许运行时长
    'MAX_RUN_TIME':4 * 24 * 60 * 60,
    # 协程池大小
    'GEVENT_POOL_SIZE':20,
    # 被允许的最大重试次数
    'MAX_RETRY_TIMES':2,
}
