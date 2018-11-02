## 基于百度站内搜索和主流招聘站点企业资料的企业官网的采集

### 任务介绍：

- **描述：**

目前，数据库中部分企业不存在官网数据，或者官网数据不规范，需要进行采集和处理。
- **步骤：**

        对于一个企业的官网数据处理流程：
        1.读取数据库中的企业官网信息。
        2.判断官网信息格式是否有效（正则）。若有效，结束。若为空，执行后续步骤。若无效，尝试从无效信息
        中进一步提取官网信息（正则）。若提取信息有效，则使用提取信息覆盖原有信息；若仍无效，执行后续步
        骤。
        3.使用百度站内搜索，尝试在各大主流招聘站点中搜索企业信息。
        4.从搜索到的企业资料中提取有效的官网信息，并对原始数据进行更新。
- **应用**：

        1.完善了企业的信息维度，便于对企业进行评估。
        2.给基于官网进行email采集的程序提供数据基础。
- **优先级：**
一般。

- **个人优先级**：高
- **问题：**

    
1. 采集的企业官网是官网具体信息，还是官网链接？

    答： 官网url


2. 读取的是哪个数据库企业官网信息？

    答：线上库的lz_datastore数据库里面的et_info表
    
    
## 任务实施：

### 基本思路：

1. 读取数据库lz_datastore中的表et_info的etid，etname，etwebsite字段 
2. 判断etwebsite字段是否存在
    - 若存在，则进行正则匹配
        - 提取到数据，将获得url更新到etwebsite
        - 不符合正则，站内搜索
    - 若不存在，则进行站内搜索
3. 站内搜索，提取官网url
    - 若提取到官网信息，即停止搜索
    - 若未提取到url，则存数据为空
    

### 代码部分：


    1. 连接数据库
        输入：无
        输出：conn，cursor
        
    2. 提取数据库信息
        输入：conn，cursor
        输出：et_dates (原公司信息)
        
    3. 处理公司信息
        输入：et_dates （原公司信息）
        输出：company （将需要进行站内搜索输出，其他的直接更新）
        
    4. 站内搜索
        输入：company
        输出：company
        
    5. 存入数据库
        输入：et_date，conn
        输出：无
        
    6.关闭数据库
        输入：conn，cursor
        输出：无
        
### 遇到的问题：
**mysql数据库更换一条数据的方法**

        
    def replace_db(conn, item, table_name):
        """
        向数据库更新一条数据的方法
        :param item: 要写入数据库的数据字典
        :param table_name: 表名
        :return:
        """
        cur = conn.cursor()
        sql1 = "update %s " % table_name
        sql2 = "set "
        for key in item.keys():
            date = item[key]
            if key == 'etid':
                sql3 = ' where %s = "%s"' % (key, date)
            else:
                sql2 += '%s = "%s",' % (key, date)
        sql = sql1 + sql2[:-1] + sql3
        # print sql
        try:
            print '正在存储、、'
            # print sql
            cur.execute(sql)
            
**分批处理：**
1. 一批etid
2. 提取一部分etid，根据etid在线上表里面提取对应信息放到一张表中并赋予状态
3. 将对应的信息进行处理
4. 更新到线上表


**在别的文件里面调用文件里面的字典：**

和调用函数差不多,例如调用settings里面的字典dict

    import settings
    print settings.dict