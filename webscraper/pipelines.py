# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re

class WebscraperPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            adapter[field_name] = value.strip()

        price= adapter.get('price', None)
        if price:
            match = re.search(r'\d+', price)
            if match:
                adapter['price'] = float(match.group())
            else:
                adapter['price'] = None

        volume = adapter.get('volume', None)
        if volume:
            match = re.search(r'\d+', volume)
            if match:
                adapter['volume'] = int(match.group())
            else:
                adapter['volume'] = None
                
        return item


import sqlite3

class SavetoSQLitePipeline:

    def __init__(self):
        self.conn = sqlite3.connect('parfume.db')
        self.cur = self.conn.cursor()

        create_table = """    CREATE TABLE IF NOT EXISTS parfume 
                              (id integer PRIMARY KEY AUTOINCREMENT,
                              parfume varchar(250),
                              price decimal(6,2),
                              category varchar(250),
                              volume integer,
                              url text)
                            """
        #drop_table = """DROP TABLE IF EXISTS parfume"""
        #self.cur.execute(drop_table)
        self.cur.execute(create_table)

    def process_item(self, item, spider):
        insert_query = """
        INSERT INTO parfume(parfume, category ,price, volume, url)
        VALUES (?, ?, ?, ?, ?)"""
        params = (item['parfume'], item['category'], item['price'], item['volume'], item['url'])
        self.cur.execute(insert_query, params)
        self.conn.commit()
        return item

def close_spider(self, spider):
    self.cur.close()
    self.conn.close()
