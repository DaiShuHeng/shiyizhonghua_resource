# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv

class ShiyizhonhuaPipeline:

    def __init__(self):
        self.f = open('gushi.csv', 'a', encoding='utf-8', newline='')
        fieldnames = ['title', 'author', 'time', 'content']
        self.csv_writer = csv.DictWriter(self.f, fieldnames)
        self.csv_writer.writeheader()

    def process_item(self, item, spider):
        d = dict(item)
        self.csv_writer.writerow(d)
        return item

    def close_spider(self, spider):
        self.f.close()
