# -*- coding: utf-8 -*-

"""
Author:by 王林清 on 2021/11/2 21:32
FileName:insertMongodb.py in chinese-poetry
Tools:PyCharm python3.8.4
"""
from pymongo import MongoClient

from util import *

if __name__ == '__main__':
    dir_name = r'./../database_json'
    paths = get_file_path(dir_name)
    print(paths)
    client = MongoClient(host='47.98.214.74', port=27017)
    with client:
        db = client['shiyizhonghua']
        db.authenticate('rw', 'cczu193rw')
        collection = db.test
        collection.drop()
        for path in paths:
            data = get_json(path)
            collection.insert_many(data)
