# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb



class LagouPipeline(object):
    def open_spider(self,spider):
        db = spider.settings.get('MYSQL_DB_NAME','lagouspider')
        host = spider.settings.get('MYSQL_HOST','localhost')
        port = spider.settings.get('MYSQL_PORT',3306)
        user = spider.settings.get('MYSQL_USER','test')
        passwd = spider.settings.get('MYSQL_PASSWORD','1234')
        self.db_conn = MySQLdb.connect(host=host,port=port,db=db,user=user,passwd=passwd,charset='utf8')
        self.db_cur = self.db_conn.cursor()

    def close_spider(self,spider):
        self.db_conn.commit()
        self.db_conn.close()

    def process_item(self, item, spider):
        self.insertdb(item)
        return item

    def insertdb(self,item):
        values =(
            item['position_name'],
            item['city'],
            item['company_name'],
            item['salary'],
            item['work_years'],
            item['company_industry'],
        )
        sql = 'INSERT INTO lagouspider VALUE (%s,%s,%s,%s,%s,%s)'
        self.db_cur.execute(sql,values)
