# spider_tianyancha_et_info


# 概述：

1. 从线上获取企业全名和etid放到线下的状态表
2. 从状态表中获取企业名称，在天眼查中搜索，并爬取其企业信息存储到数据库中

### 任务要求：

获取天眼查中的企业信息

### 任务记录:
1. 使用scrapy框架去写此爬虫
2. 暂时放弃使用scrapy框架来写这个爬虫
3. 先使用一般的python来写
4. 设计数据表：企业总表，工商信息表等
5. **注意**：需要添加融资的信息，以及如何从数据库分批拿信息（解决）

分部执行任务：

1. 解析全部的信息
2. 建立各个表格
3. 获取对应企业信息
4. 连接数据库

### 爬虫思路：

1. 先获取需要采集信息的公司：
    1. 从线上数据库lz_datastore中的表et_info中获取
    2. 获取字段：etid，etname
    3. 将获取的数据存储到线下的状态表中
    4. 从状态表中获取数据，并更新状态表
2. 拼接初始URL：
    1. 将etname和初始url进行拼接，获得初始网址
3. 请求解析初始一级页面：
    1. 验证查询的公司是否正确（？？）
    2. 获取二级页面url
4. 请求解析二级页面：
    1. 获取的信息待定
5. 将公司的信息存储到数据库中：
    1. 建表
    2. 存储信息


### 所建的表：

**所建的表目前都放在线下spider库中**

1. 企业主要信息：   et_host_info
2. 工商信息：       et_busi_info
3. 分支机构信息：   et_branch_office
4. 软件著作权信息： et_container_copyright_info
5. 网站备案信息：   et_conrainer_icp_info
6. 对外投资信息：   et_foreign_investment_info
7. 融资信息：       et_rongzi_info
8. 股东信息：       et_stareholder_info
9. 商标信息：       et_trademark_info
10. 微信公众号信息：et_wechat_list_info

### 可以获取到的信息：

- **网址**：
    - a class="company-link" /text()
- **地址**：
    - span class="address" /@title
- **简介**：
    - script id="company_base_info_detail" /text()
- **法定代表人**：
    - .xpath("//div[@class='humancompany']/div[@class='name']/a/text()")
- **公司状态：存续**
    - xpath("//div[@class='num-opening']/text()")
- **工商信息：**  （单独建表）
    - 除了经营范围不能获取，其他可获取
- **主要人员：**
    - 均可获取
- **股东信息：** （单独建表）
    - 均可获取
- **对外投资：** （单独建表）
    - 均可获取
- **最终受益人：**  （信息和股东信息差不多，未取）
    - 均可获取
- **分支机构：** （单独建表）
    - 可获取
- **微信公众号：**
    - 可获取
- **商标信息：** （需要取图片，未取）
    - 可获取
- **软件著作权：**
    - 可获取
- **网站备案：**
    - 可获取



### 涉及到的知识：
1. response.url：表示获取这个返回html的url（目前已知实用于scrapy）
2. Python rstrip() 删除 string 字符串末尾的指定字符（默认为空格）.
rstrip()方法语法：
```
    str.rstrip([chars])
```

3. 测试过，在xpath中可以使用%s
4. 为什么字典覆盖赋值的时候不变？？
5. （**重点**）list在append字典的时候是传递的字典的地址，在传递相同名字的字典的时候要注意，要重新定义一个字典item={}
> 在其他语言中，你去定义一个变量的时候，是为变量开辟一个空间，而在python中不一样，python是为值来开辟空间
6. 如何忽略警告：

直接将下面的代码直接放到代码的最前面即可

```
import warnings
warnings.filterwarnings("ignore")
```
