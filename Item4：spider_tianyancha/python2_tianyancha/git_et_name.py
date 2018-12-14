#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:吉祥鸟
# datetime:2018/11/7 15:53
# software: PyCharm

import sys
import hu_utils
reload(sys)
sys.setdefaultencoding('utf8')


def get_etid():
    conn = hu_utils.open_line_db()
    et_namess = hu_utils.select_ones(conn)
    for et_names in et_namess:
        et_nams = []
        print len(et_names)
        for et_name in et_names:
            if et_name[1]:
                et_nam = {}
                et_nam["etid"] = et_name[0]
                et_nam["et_name"] = et_name[1]
                et_nams.append(et_nam)
        conn = hu_utils.open_local_db()
        hu_utils.insert_ignore_many(conn, et_nams, "et_name_status")


def main():
    get_etid()

if __name__=="__main__":
    main()
