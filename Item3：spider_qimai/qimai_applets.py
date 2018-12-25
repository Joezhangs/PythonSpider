# -*- coding: UTF-8 -*-
# author:吉祥鸟
# datetime:2018/12/25 14:12
# software: PyCharm

from qimai import get_chrome
from selenium.webdriver.support.ui import WebDriverWait
import logging
from selenium.webdriver.support import expected_conditions as EC
import hu_utils
import time

logger = logging.getLogger(__name__)


def main():
    try:
        browser = get_chrome()  # 获取chrome
        browser.maximize_window()  # 全屏浏览器界面
        url = "https://www.qimai.cn/weixin/miniapp"
        browser.get(url)
        browser.implicitly_wait(10)
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_all_elements_located(("xpath", "//tbody")))
        time.sleep(3)
        tbody = browser.find_element("xpath", "//tbody")
        trs = tbody.find_elements("xpath", "tr")  # 100条信息
        print(len(trs))
        applets_infos = []
        t = 0
        for tr in trs:
            applets_info = {}
            t += 1
            print("正在获取第{}条数据".format(t))
            a = tr.find_elements("xpath", "td[2]/div/a")
            full_info_link = a[0].get_attribute('href')  # 详情url
            logo = a[0].find_element_by_xpath("img").get_attribute('src')  # logo
            name = a[0].find_element_by_xpath("p").text  # 小程序名称
            applets_type = tr.find_elements_by_xpath("td[3]/div")[0].text  # 服务类别
            print(applets_type)
            try:
                et_name_a = tr.find_elements_by_xpath("td[4]/a")[0]
                et_name = et_name_a.text  # 公司名称
                print(et_name)
                et_link = et_name_a.get_attribute("href")  # 公司链接
            except:
                print("公司信息获取出错，可能没有公司这类信息")
            applets_num = tr.find_elements_by_xpath("td[5]/div")[0].text  # 小程序指数
            applets_info["full_info_link"] = full_info_link
            applets_info["logo"] = logo
            applets_info["name"] = name
            applets_info["et_link"] = et_link
            applets_info["et_name"] = et_name
            applets_info["applets_num"] = applets_num
            applets_info["applets_type"] = applets_type
            applets_infos.append(applets_info)
            if t == 101:
                break
    finally:
        logger.info("关闭浏览器")
        browser.close()
        conn = hu_utils.open_local_db(db="app_info")
        hu_utils.insert_update_many(conn, applets_infos, "applets_info")


main()
