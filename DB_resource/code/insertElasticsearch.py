# -*- coding: utf-8 -*-

"""
Author:by 王林清 on 2021/11/25 18:13
FileName:insertElasticsearch.py in shiyizhonghua_resource
Tools:PyCharm python3.8.4
"""
from elasticsearch import Elasticsearch, helpers

from util import *

if __name__ == '__main__':
    dir_name = r'./../database_json'
    paths = get_file_path(dir_name)
    es = Elasticsearch(hosts=['114.55.236.49:9200'], timeout=60)
    index_name = 'shiyizhonghua'
    paths = paths[:]
    total = len(paths)
    for path in paths:
        datas = get_json(path)
        bulk_data = []
        for data in datas:
            bulk_data.append(
                {
                    '_index': index_name,
                    '_source': data
                }
            )
        helpers.bulk(es, bulk_data)
        file_name = path.replace('./../database_json\\', '')
        print(f"{file_name:<18}导入成功,还有{total:<3}个文件待导入!")
        total -= 1
