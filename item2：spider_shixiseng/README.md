**使用requests爬取实习僧网站数据**

**任务要求：**

爬取实习僧网站的招聘公司信息和职位信息，并存储到数据库中，对应的数据库表和需要爬取的字段见下面表一和表二（注意：爬取存在的字段）


### 看一下爬下来的结果图：

**公司信息：**

![image](http://paxd6g86d.bkt.clouddn.com/bk/2018-09-19_180559.png)

**职业信息：**

![image](http://paxd6g86d.bkt.clouddn.com/bk/2018-09-19_180711.png)



## 1. 检查是否有api

无

## 2. 确定数据分析和数据存储


- **确定构建的表和连接关系**


	    表一：dt_company

	    ID: id
	    采集对象编号：doid
	    所属站点：site
	    公司名称：company_name
	    注册时间：company_regtime
	    成立时间：company_uptime
	    公司性质：company_kind
	    所属行业：company_industry
	    注册资金：company_capital
	    员工人数：company_workers
	    所在地：company_area
	    邮政编码：company_postcode
	    公司联系人：company_ecname
	    公司电话：company_phone
	    手机号码：company_mobile
	    公司传真：company_fax
	    公司地址：company_address
	    公司网址：company_website
	    电子邮箱：company_email
	    公司描述：company_detail
	    最后更新时间：company_updatetime
	    企业状态：status
	    采集源url：url
	    采集时间:addtime
	    更新时间:updatetime
	    对应乐职网etid:etid
	    对应乐职网企业名称:etname
	    类别:type


	    表二：dt_jobs_2

	    site  varchar(16) NOT NULL站点
	    doid  varchar(56) NOT NULL采集对像编号
	    company_name  varchar(256) NOT NULL企业名称
	    job_name  varchar(256) NOT NULL职位名称
	    job_updatetime  int(11) NOT NULL更新时间
	    job_starttime  int(11) NOT NULL发布日期
	    job_endtime  int(11) NOT NULL结止日期
	    company_industry  varchar(56) NOT NULL所在行业
	    job_type  varchar(128) NOT NULL职位类别
	    company_kind  varchar(56) NOT NULL企业类型
	    job_area  varchar(128) NOT NULL工作地点
	    job_mode  varchar(56) NOT NULL工作类型
	    job_year  varchar(56) NOT NULL工作年限
	    job_money  varchar(56) NOT NULL工资
	    job_degree  varchar(56) NOT NULL学历
	    job_sex  varchar(56) NOT NULL性别
	    job_age1  varchar(56) NOT NULL要求年龄
	    job_age2  varchar(56) NOT NULL
	    job_lang  varchar(56) NOT NULL外语要求
	    job_major  varchar(56) NOT NULL专业要求
	    job_rest  varchar(56) NOT NULL是否双休
	    job_welfare  varchar(56) NOT NULL五险一金
	    job_mail  varchar(56) NOT NULL邮箱地址
	    job_detailed  text NOT NULL工作详细
	    job_demand text NOT NULL工作要求
	    job_num varchar(56) NOT NULL招聘人数
	    job_department  varchar(56) NOT NULL所属部门
	    addtime int(11) NOT NULL采集时间
	    updatetime int(11) NOT NULL更新时间
	    url varchar(128) NOT NULL采集源url
	    statustiny int(1) NOT NULL职位状态 -9周伯通职位暂不处理
	    etid  int(11) NOT NULL对应乐职网etid
	    etjobid  int(11) NOT NULL对应乐职网职位ID
	    etjobname  varchar(128) NOT NULL对应乐职网职位名称
	    job_report  varchar(56) NOT NULL汇报对象
	    job_reportnums  varchar(32) NOT NULL下属人数
	    job_coreskills  varchar(256) NOT NULL技能关键字
	    isheadhuntertiny  int(4) NOT NULL是否猎头职位：1是，0否


- **选择需要连接的数据库**

mysql

## 3. 数据流分析


- **确定爬取的范围**

部分页

- **切入源头**

https://www.shixiseng.com/interns?k=&t=zj&p=1

- **多层网络结构间跳转流程**

更改参数p进行爬取


- **范围细分**

无

## 4. 数据采集


- **请求模块**


requests

- **解析工具**

xpath


- **数据存储**

mysql
- **爬虫效率提升问题**

使用多协程



## 5. 反反爬虫
会有请求失败的问题：
    通过添加请求头解决


## 遇到的问题：
	
	1. 在爬取的字符串数据中值需要一部分：
		使用split将字符串进行切割
	2. 判断爬取的数据是否是你需要的：
		使用if判断a字符串是否在b中
	3. 爬取停止：
		sys.exit('tingzhi')

    4.crontab定时任务：
        - 先vim /var/spool/cron/root  （打开这个文件）
        - 添加任务：
            每天的第一个小时的第一个分钟执行
            1 1*** python /root/lezhi/爬取实习僧/spider_shixiseng.py
        - esc 之后 ：wq保存退出
    
    **部署问题：**
        screen -x 20156  （打开后台状态为 Attached 且名称为 django 的 screen shell）
        
        vim 编译器
            ：  （冒号进入编译模式）
                q 退出
                w 保存
                i 编辑
                
        screen -X -S 4588 quit  (杀死一个已经detached的screen会话  )
