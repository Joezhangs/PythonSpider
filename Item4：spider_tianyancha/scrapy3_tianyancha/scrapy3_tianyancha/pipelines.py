# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymysql
import scrapy
import traceback
logger = logging.getLogger(__name__)


class MysqlPipeline_stop(object):
    """
    这个类是之前写的，用于单个item插入
    """

    def __init__(self, host=None, database=None, user=None, password=None, port=None):  # 定义函数变量
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self, spider):
        print("开启数据库")
        logger.info("开启数据库")
        # print(self.host, self.database, self.user, self.password, self.port)
        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.database,  # 数据库名
            charset="utf8",
        )
        print(self.conn)
        print("开启完成")
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        print("关闭数据库")
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        print("更新数据表{}.....".format(item.table))
        print("item:", item)
        if item:
            sql1 = "insert into %s" % item.table
            sql2 = "("
            sql3 = ") values("
            sql4 = ")on duplicate key update "
            for key in item.keys():  # 拼接sql语句
                sql2 += "%s," % key
                sql3 += "%s,"
                sql4 += "%s=values(%s)," % (key, key)
            # try:
            item_values = list(item.values())
            item_values[1] = str(item_values[1])
            # print item_values
            sql = sql1 + sql2[:-1] + sql3[:-1] + sql4[:-1]
            # print(sql)
            self.cursor.execute(sql, item_values)
            self.conn.commit()
            print("数据更新成功")
            # except:
            #     print('更新数据失败，回滚')
            #     self.conn.rollback()
        return item


class MysqlPipeline(object):
    def __init__(self, db_host, db_port, db_user, db_passwd, db_name, item_class_list):
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_passwd = db_passwd
        self.db_name = db_name
        self.item_list = {}  # 包含数据的列表
        self.batch_size = 100
        self.item_class_list = item_class_list

    @classmethod
    def from_crawler(cls, crawler):
        db_host = crawler.settings.get('MYSQL_HOST')
        db_port = crawler.settings.get('MYSQL_PORT')
        db_user = crawler.settings.get('MYSQL_USER')
        db_passwd = crawler.settings.get('MYSQL_PASSWORD')
        db_name = crawler.settings.get('MYSQL_DATABASE')
        item_class_list = crawler.settings.get('MYSQL_PIPELINE_ITEM_CLASS_LIST')
        return cls(db_host=db_host, db_port=db_port, db_user=db_user, db_passwd=db_passwd, db_name=db_name,
                   item_class_list=item_class_list)

    def get_mysql_conn(self):
        """
        创建数据库连接
        :return:
        """
        print("连接数据库")
        logger.info("开启数据库")
        conn = pymysql.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_passwd,
            port=self.db_port,
            db=self.db_name,
            use_unicode=True,
            charset="utf8"
        )
        return conn

    def insert_many(self, table_name, item_list):
        """
        批量写入到数据库
        :param table_name:
        :param item_list:
        :return:
        """
        # 转化数据格式，以方便写入
        print("写入数据库{}数据{}条".format(table_name, len(item_list)))
        logger.info("写入数据库{}数据{}条".format(table_name, len(item_list)))
        item = item_list[0]
        key_list = []
        for key, value in item.items():
            key_list.append(key)
        # sql = f"insert ignore {table_name}({','.join(key_list)}) " \
        #       f"values({','.join(['%s' for _ in range(len(key_list))])})"
        sql = "insert ignore {}({}) values({})".format(table_name, ','.join(key_list),
                                                       ','.join(['%s' for _ in range(len(key_list))]))
        insert_list = []
        for item in item_list:
            insert_list.append([item[key] for key in key_list])
        # 批量写入数据库
        conn = self.get_mysql_conn()
        cursor = conn.cursor()
        try:
            cursor.executemany(sql, insert_list)
            conn.commit()
            print("写入成功")
            logger.info("写入成功")
        except Exception as e:
            print("出错，重写数据")
            logger.info("出错，重写数据")
            conn.rollback()
            traceback.print_exc()
        cursor.close()
        conn.close()
        self.item_list[table_name].clear()

    def insert_update_many(self, items, table_name):
        """
        多条数据插入或更新到数据库（注：插入的数据包含表里的关键字）
        :param conn:数据库
        :param items:插入的数据列表字典（列表内包含字典类型）
        :param table_name:数据库表名
        :return:无
        """
        print("更新数据表{}...".format(table_name))
        logger.info("更新数据表{}...".format(table_name))
        conn = self.get_mysql_conn()
        # print("item:", items)
        if items:
            cursor = conn.cursor()
            sql1 = "insert into %s" % table_name
            sql2 = "("
            sql3 = ") values("
            sql4 = ")on duplicate key update "
            for key in items[0].keys():  # 拼接sql语句
                sql2 += "%s," % key
                sql3 += "%s,"
                sql4 += "%s=values(%s)," % (key, key)
            sql = sql1 + sql2[:-1] + sql3[:-1] + sql4[:-1]
            item_values = []
            for item in items:
                item_values.append(list(item.values()))
            num = len(item_values)
            print('一共需要处理数据%s条' % num)
            try:
                for i in range(0, num, 1000):
                    a = min(num, 1000 + i)
                    cursor.executemany(sql, item_values[i:a])
                    conn.commit()
                    print("当前已经处理%s条数据" % a)
            except:
                print('更新数据失败，回滚')
                logger.info('更新数据失败，回滚')
                conn.rollback()
        cursor.close()
        conn.close()
        self.item_list[table_name].clear()

    def insert_to_db(self):
        """
        将数据加入到列表中，
        并调用写入方法
        :return:
        """
        for table_name, item_list in self.item_list.items():  # list.items()可以遍历的元组
            # print("{}:{}".format(table_name, len(item_list)))
            if len(item_list) >= self.batch_size:
                if table_name == "et_name_status":
                    self.insert_update_many(item_list, table_name)
                else:
                    self.insert_many(table_name, item_list)

    def process_item(self, item, spider):
        """
        处理项目
        :param item:
        :param spider:
        :return:
        """
        if getattr(getattr(item, '__class__'), '__name__') in self.item_class_list:  # 返回一个对象的属性值
            self.item_list.setdefault(item.table_name, []).append(item)  # 若不存在则添加键，并谁为默认值
            # print("itemlist:",self.item_list)
            self.insert_to_db()
        return item

    def close_spider(self, spider):
        self.batch_size = 1
        self.insert_to_db()
