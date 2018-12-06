
实习期间，公司安排了一个简单的任务，下面是任务要求：

### 任务要求： ###
**基于招聘站点和企业名称的 email采集**

	1. 获取一批要采集email的企业
	2. 使用百度，在各大招聘站点内部搜索要采集的企业的招聘页面。
	3. 从招聘页面提取出企业的email（需要排除招聘站点官方、猎头相关的email）。
	4. 将采集的结果保存到数据库

理一下大概的思路

### 基本思路： ###

1. 初始url分几钟：智联，猎聘，大街，前程无忧，中华英才网 这些都是需要进行单个站点的解析分别编写代码
2. 连接数据库提取企业名称，插入url，进行get请求
	- get_url_html 请求模块
3. 解析各个站点获取信息
    - 如何判断？？存在网页信息不对称
4. 信息进行正则匹配，匹配email
	- get_emails 模块
5. 存到数据库




### 爬虫流程： ###
1. 检查是否有api

	无

2. 切入源头

    百度内部搜索多个站点
	https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&rsv_idx=1&tn=93153557_hao_pg&wd=site%EF%BC%9Ashixiseng.com%20%E9%98%BF%E9%87%8C

3. 爬取的范围

	爬取的是需要采集的企业的email

4. 多层网络结构间跳转流程

	先源头搜索
```
graph LR
单个公司-->单个站点搜索1
单个站点搜索1-->二级页面1
单个站点搜索1-->二级页面2
二级页面1-->三级页面1
二级页面1-->........
二级页面1-->三级页面n
二级页面2-->三级页面m
二级页面2-->.........
二级页面2-->三级页面m+n

```


5. **选择需要连接的数据库和表**

	连接的表et_ema的DDL信息：
	    
        CREATE TABLE `et_ema` (
          `id` int(12) NOT NULL AUTO_INCREMENT COMMENT 'ID',
          `etid` int(11) NOT NULL COMMENT '序号',
          `email` varchar(50) NOT NULL DEFAULT '' COMMENT '公司email',
          PRIMARY KEY (`id`),
          UNIQUE KEY `etid,email` (`etid`,`email`)
        ) ENGINE=InnoDB AUTO_INCREMENT=1776 DEFAULT CHARSET=gbk ROW_FORMAT=DYNAMIC COMMENT='公司email'


6. **确定爬取的字段和连接关系**

    公司
    
    email

## 数据采集 ##


- **常用模块**

    request

- **解析工具**

    xpath
- **数据存储**

    mysql
    
- **爬虫效率提升问题**

    简单使用多协程


### 代码大纲： ###

**main函数：**
    
    1. 连接数据库
        输入：无
        输出：conn，cursor
    2. 获取公司信息：etid，etname
        输入：cursor
        输出：companys
    3. 站点代码：获取网页信息，1，2，3
        输入：url
        输出：text
    4. 正则email，并去重
        输入：text
        输出：emails
    5. 存入数据库：一次存入一条信息
        输入：conn, companys_email, table_name
        输出：无
    6. 关闭数据库
        输入：conn，cursor
        输出：无
    


## 遇到的问题：

**正则匹配的问题**：

    1. 不匹配括号里的内容的方法：使用 ？：
    2. [...]可以匹配【】中的任意字符，如[abc]即匹配a,b,c的任意一个字符
    3. findall匹配后不能使用group
    
**字典和文件格式转换：**

    1.json.dumps	将 Python 对象编码成 JSON 字符串
    2.json.loads	将已编码的 JSON 字符串解码为 Python 对象
    3. 读取txt文件里的字典(打开，read，load，关闭)
        file = open('text.txt', 'r')
        js = file.read()
        dic = json.loads(js)
        print (dic)
        file.close()
    4. 字典写入txt：
        dic = {  
            'andy':{  
                'age': 23,  
                'city': 'beijing',  
                'skill': 'python'  
            },  
            'william': {  
                'age': 25,  
                'city': 'shanghai',  
                'skill': 'js'  
            }  
        }  
        
        js = json.dumps(dic)   
        file = open('test.txt', 'w')  
        file.write(js)  
        file.close()  

**screen的用法：**

    screen：可以通过该软件同时连接多个本地或远程的命令行会话，并在其间自由切换，可以后台运行爬虫
    后台运行爬虫的步骤：
    1. 直接运行爬虫
        screen python run.py
    2. 退出保存窗口
        ctrl+a+d 
    3. 查看打开的screen（意思的‘屏幕’）
        screen -ls
    4. 重新打开关闭的screen
        screen -r 50126
        
**xpath匹配问题：**

    一属性多值：[contains(@class, "li")]
    
**对于如何将edid对应：**

    获取的时候同时将etid和etname从数据库中拿出来，之后存储的时候再一起存进去
    
**如何去除list中重复的元素：**

    使用内置的set函数：
        i = ['b','c','d','b','c','a','a']
        z = list(set(i))
        print z
        
**在数据库中建立表：**

    CREATE TABLE IF NOT EXISTS `et_email` (
        `id` INT(12) NOT NULL AUTO_INCREMENT COMMENT 'ID',
        `etid` INT(11) NOT NULL COMMENT '序号',
        `email` VARCHAR(30) NOT NULL DEFAULT '' COMMENT '公司email',
        PRIMARY KEY (`id`),`et_email`
        KEY (`etid`)
    ) ENGINE=INNODB DEFAULT CHARSET=gbk ROW_FORMAT=DYNAMIC COMMENT='公司email'

    replace into et_email(etid,email) values('100224953','emma.chn@unilever.com')
    replace into et_email(etid,email) values('2817270','u81f3hr_sytate@163.com')
    
**多协程的问题：**

    gevent.pool不能进行多参数的传递，可以使用from functools import partial来进行多参数的传递
    使用方法：  
        def run (a,b):
            pass
        partial.work = partial(run, a)
        gevent.pool.map(partial.work,b)
    (注意：
    partial不能有迭代的参数
    map函数是需要是以迭代的方式来对b进行数据的提取，以后以参数的形式调用
    如果有多个需要迭代的参数，可以使用z = zip（a，b）)