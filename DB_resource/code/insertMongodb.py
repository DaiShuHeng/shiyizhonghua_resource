# -*- coding: utf-8 -*-

"""
Author:by 王林清 on 2021/11/2 21:32
FileName:insertMongodb.py in shiyizhonghua_resource
Tools:PyCharm python3.8.4
"""
from pymongo import MongoClient

from util import *

if __name__ == '__main__':
    dir_name = r'./../database_json'
    paths = get_file_path(dir_name)
    host = '114.55.236.49'
    client = MongoClient(host=host, port=27017,
                         username='rw', password='cczu193rw',
                         authSource='shiyizhonghua')
    with client:
        db = client['shiyizhonghua']
        collection = db['data']
        collection.drop()
        for path in paths:
            data = get_json(path)
            collection.insert_many(data, ordered=False)

