# -*- coding: UTF-8 -*-
# author:吉祥鸟
# datetime:2018/12/25 11:03
# software: PyCharm
from qimai import get_chrome
from selenium.webdriver.support.ui import WebDriverWait
import logging
from selenium.webdriver.support import expected_conditions as EC
import hu_utils

logger = logging.getLogger(__name__)


def main():
    try:
        browser = get_chrome(True)  # 获取chrome
        browser.maximize_window()  # 全屏浏览器界面
        url = "https://www.qimai.cn/weixin"
        browser.get(url)
        browser.implicitly_wait(10)
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_all_elements_located(("xpath", "//p[@class='medium-txt']")))
        trs = browser.find_elements("xpath", "//tr[@class='ivu-table-row']")  # 100条信息
        public_accounts_infos = []
        for tr in trs:
            public_accounts_info = {}
            public_accounts_name = tr.find_element("xpath", "td//p[@class='medium-txt']").text
            et_name = tr.find_element("xpath", "td[3]/div/span").text
            strength_value = tr.find_element("xpath", "td[4]/div/span").text
            public_accounts_info["name"] = public_accounts_name
            public_accounts_info["et_name"] = et_name
            public_accounts_info["strength_value"] = strength_value
            print(public_accounts_info)
            public_accounts_infos.append(public_accounts_info)
    finally:
        logger.info("关闭浏览器")
        browser.close()
        conn = hu_utils.open_local_db(db="app_info")
        hu_utils.insert_update_many(conn, public_accounts_infos, "public_accounts_info")


main()
