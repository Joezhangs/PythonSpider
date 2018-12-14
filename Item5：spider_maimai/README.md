
**代码已经上传到[github](https://github.com/huquan1996/PythonSpider/tree/master/Item5%EF%BC%9Aspider_maimai)上**

## 简介：

这是一个基于python3而写的爬虫，爬取的网站的脉脉网([https://maimai.cn/](https://maimai.cn/))，在搜索框中搜索“CHO”，并切换到“人脉”选项卡，点击姓名，进入详情页，爬取其详细信息

![image](https://hqx.oss-cn-beijing.aliyuncs.com/image/20181213094449.jpg?x-oss-process=style/narrow50_50)

### 获取的具体信息有：

基本信息、工作经历、教育经历、职业标签及其认可数、点评信息

几度关系：一度、二度、三度等

## 写给用户的

**注意：如果你只是想使用这个项目，那么你可以看这里**

### 如何使用：

#### 使用之前，你要已经保证安装好相关的库和软件：

1. re
2. requests
3. selenium
4. logging
5. pymysql
5. chrome
6. mysql

#### 使用：
1. **从github上复制代码**
2. **填写自己的脉脉手机号和密码（你可以在login.py文件中找到他）**
![image](https://hqx.oss-cn-beijing.aliyuncs.com/image/360_20181213134448.jpg?x-oss-process=style/narrow100_100)
3. **建表（详细建表见下）**
43. **运行程序login.py**

### 详细建表

**需要5张表，下面附上代码：**
- 表1：basic_info(脉脉好友基本信息)
```
CREATE TABLE `basic_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `name` varchar(56) NOT NULL COMMENT '名字',
  `mmid` int(11) NOT NULL COMMENT 'mmid',
  `rank` int(11) DEFAULT NULL COMMENT '影响力',
  `company` varchar(128) DEFAULT NULL COMMENT '目前公司简称',
  `stdname` varchar(128) DEFAULT NULL COMMENT '目前公司全称',
  `position` varchar(128) DEFAULT NULL COMMENT '目前职位',
  `headline` text COMMENT '自我介绍',
  `ht_province` varchar(128) DEFAULT NULL COMMENT '家乡-省',
  `ht_city` varchar(128) DEFAULT NULL COMMENT '家乡-城市',
  `email` varchar(128) DEFAULT NULL COMMENT '邮箱',
  `mobile` varchar(128) DEFAULT NULL COMMENT '手机',
  `dist` tinyint(1) DEFAULT NULL COMMENT '几度关系',
  PRIMARY KEY (`id`),
  UNIQUE KEY `mmid` (`mmid`)
) ENGINE=InnoDB AUTO_INCREMENT=873 DEFAULT CHARSET=gbk ROW_FORMAT=DYNAMIC COMMENT='脉脉好友基本信息'
]

```

- 表2：education_exp(脉脉好友教育经历)
```
CREATE TABLE `education_exp` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `mmid` int(11) NOT NULL COMMENT 'mmid',
  `school_name` varchar(128) DEFAULT NULL COMMENT '学校名称',
  `department` varchar(128) DEFAULT NULL COMMENT '专业',
  `education` int(5) DEFAULT NULL COMMENT '学历（0：专科，1：本科，2：硕士，3：博士，255：其他）',
  `start_year` int(11) DEFAULT NULL COMMENT '开始时间（年）默认为0000',
  `start_mon` int(11) DEFAULT NULL COMMENT '开始时间（月）默认为0000',
  `end_year` int(11) DEFAULT NULL COMMENT '结束时间（年）默认为0000',
  `end_mon` int(11) DEFAULT NULL COMMENT '结束时间（月）默认为0000',
  PRIMARY KEY (`id`),
  UNIQUE KEY `mmid` (`mmid`,`school_name`,`education`,`start_year`)
) ENGINE=InnoDB AUTO_INCREMENT=1064 DEFAULT CHARSET=gbk ROW_FORMAT=DYNAMIC COMMENT='脉脉好友教育经历'
```

- 表3：review_info(脉脉好友点评信息)

```
CREATE TABLE `review_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `mmid` int(11) NOT NULL COMMENT 'mmid',
  `reviewer` varchar(128) DEFAULT NULL COMMENT '点评人',
  `relationship` varchar(128) DEFAULT NULL COMMENT '关系',
  `position` varchar(128) DEFAULT NULL COMMENT '点评人职位',
  `eva_info` text COMMENT '评价信息',
  PRIMARY KEY (`id`),
  UNIQUE KEY `mmid` (`mmid`,`reviewer`)
) ENGINE=InnoDB AUTO_INCREMENT=400 DEFAULT CHARSET=gbk ROW_FORMAT=DYNAMIC COMMENT='脉脉好友点评信息'

```
- 表4：tag_info(脉脉好友点评信息)
```
CREATE TABLE `tag_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `mmid` int(11) NOT NULL COMMENT 'mmid',
  `tag` varchar(128) DEFAULT NULL COMMENT '标签',
  `rec_num` varchar(128) DEFAULT NULL COMMENT '认可度',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQUE` (`mmid`,`tag`,`rec_num`)
) ENGINE=InnoDB AUTO_INCREMENT=5881 DEFAULT CHARSET=gbk ROW_FORMAT=DYNAMIC COMMENT='脉脉好友点评信息'

```

- 表5：work_exp(脉脉好友工作经历)
```
CREATE TABLE `work_exp` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `mmid` int(11) NOT NULL COMMENT 'mmid',
  `company` varchar(128) DEFAULT NULL COMMENT '公司简称',
  `stdname` varchar(128) DEFAULT NULL COMMENT '公司全称',
  `et_url` varchar(244) DEFAULT NULL COMMENT '公司页面url',
  `description` text COMMENT '描述',
  `start_year` int(11) DEFAULT NULL COMMENT '开始时间（年）默认0000',
  `start_mon` int(11) DEFAULT NULL COMMENT '开始时间（月）默认0000',
  `end_year` int(11) DEFAULT NULL COMMENT '结束时间（年）默认0000',
  `end_mon` int(11) DEFAULT NULL COMMENT '结束时间（月）默认0000',
  `position` varchar(128) DEFAULT NULL COMMENT '职位',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQUE` (`mmid`,`company`,`start_year`,`position`)
) ENGINE=InnoDB AUTO_INCREMENT=2582 DEFAULT CHARSET=gbk ROW_FORMAT=DYNAMIC COMMENT='脉脉好友工作经历'

```
